from mpi4py import MPI
import numpy as np
import pandas as pd
from genetic_algorithms_functions import calculate_fitness, select_in_tournament, order_crossover, mutate, generate_unique_population
import time

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Load the distance matrix only on rank 0
if rank == 0:
    distance_matrix = pd.read_csv('/home/student/DSAI-3202-LABS/Assignment1_Part2/data/city_distances.csv').to_numpy()
else:
    distance_matrix = None  # Initialize for other processes

# Broadcast the distance matrix to all processes
distance_matrix = comm.bcast(distance_matrix, root=0)

# Parameters
num_nodes = distance_matrix.shape[0]
population_size = 10000 // size  # Split among processes
num_generations = 200
mutation_rate = 0.1
stagnation_limit = 5

# Initialize population
np.random.seed(42 + rank)  # Ensure diversity across processes
population = generate_unique_population(population_size, num_nodes)

# Track best fitness
best_fitness = float('inf')
stagnation_counter = 0

# Start timing
start_time = time.time()

# Main Genetic Algorithm Loop
for generation in range(num_generations):
    # Parallel fitness evaluation
    fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in population])
    
    # Gather fitness values at root
    all_fitness_values = comm.gather(fitness_values, root=0)
    all_population = comm.gather(population, root=0)

    if rank == 0:
        # Flatten lists
        all_fitness_values = np.concatenate(all_fitness_values)
        all_population = np.concatenate(all_population, axis=0)

        # Track best solution (Elitism)
        best_idx = np.argmin(all_fitness_values)
        current_best_fitness = all_fitness_values[best_idx]

        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        if stagnation_counter >= stagnation_limit:
            print(f"Regenerating population at generation {generation} due to stagnation")
            best_individual = all_population[best_idx]
            all_population = generate_unique_population(10000 - 1, num_nodes)
            all_population.append(best_individual)
            stagnation_counter = 0

        # Perform selection, crossover, and mutation
        selected = select_in_tournament(all_population, all_fitness_values)
        offspring = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            route1 = order_crossover(parent1[1:], parent2[1:])
            offspring.append([0] + route1)
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

        # Replace worst individuals
        for i, idx in enumerate(np.argsort(all_fitness_values)[::-1][:len(mutated_offspring)]):
            all_population[idx] = mutated_offspring[i]

        # Split updated population for distribution
        new_populations = np.array_split(all_population, size)
    else:
        new_populations = None

    # Scatter new populations back to processes
    population = comm.scatter(new_populations, root=0)

    # Print best fitness at rank 0
    if rank == 0:
        print(f"Generation {generation}: Best Fitness = {best_fitness}")

# Final best solution
final_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in population])
all_fitness_values = comm.gather(final_fitness_values, root=0)
all_population = comm.gather(population, root=0)

if rank == 0:
    all_fitness_values = np.concatenate(all_fitness_values)
    all_population = np.concatenate(all_population, axis=0)

    best_idx = np.argmin(all_fitness_values)
    best_solution = all_population[best_idx]
    
    print("Best Solution:", best_solution)
    print("Total Distance:", calculate_fitness(best_solution, distance_matrix))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Parallel Execution Time: {elapsed_time:.2f} seconds")
