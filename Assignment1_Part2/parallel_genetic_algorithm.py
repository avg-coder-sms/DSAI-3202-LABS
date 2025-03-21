from mpi4py import MPI
import numpy as np
import pandas as pd
from src.genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, \
    generate_unique_population
import time

start_time = time.time()
# MPI Setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Load the distance matrix only on rank 0
if rank == 0:
    distance_matrix = pd.read_csv('/home/student/DSAI-3202-LABS/Assignment1_Part2/data/city_distances.csv').to_numpy()
else:
    distance_matrix = None  # Define it on other ranks

# Broadcast the distance matrix to all processes
distance_matrix = comm.bcast(distance_matrix, root=0)

# Parameters
num_nodes = distance_matrix.shape[0]
population_size = 10000
num_tournaments = 4
mutation_rate = 0.1
num_generations = 200
infeasible_penalty = 1e6
stagnation_limit = 5

# Generate initial population
np.random.seed(42)
population = generate_unique_population(population_size, num_nodes)

# Initialize variables for tracking stagnation
best_calculate_fitness = int(1e6)
stagnation_counter = 0

# Main GA loop
for generation in range(num_generations):
    # Parallelize fitness calculation using MPI
    chunk_size = population_size // size
    local_population = population[rank * chunk_size: (rank + 1) * chunk_size]
    local_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in local_population])
    
    # Gather all fitness values to rank 0
    all_fitness_values = comm.gather(local_fitness_values, root=0)
    
    if rank == 0:
        # Flatten the fitness values
        all_fitness_values = np.concatenate(all_fitness_values)
        
        # Check for stagnation
        current_best_calculate_fitness = np.min(all_fitness_values)
        if current_best_calculate_fitness < best_calculate_fitness:
            best_calculate_fitness = current_best_calculate_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1
        
        # Regenerate population if stagnation limit is reached
        if stagnation_counter >= stagnation_limit:
            print(f"Regenerating population at generation {generation} due to stagnation")
            best_individual = population[np.argmin(all_fitness_values)]
            population = generate_unique_population(population_size - 1, num_nodes)
            population.append(best_individual)
            stagnation_counter = 0
            continue  # Skip the rest of the loop for this generation

        # Selection, crossover, and mutation
        selected = select_in_tournament(population, all_fitness_values)
        offspring = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            route1 = order_crossover(parent1[1:], parent2[1:])
            offspring.append([0] + route1)
        
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]
        
        # Replacement (rank 0 applies the best mutated offspring)
        for i, idx in enumerate(np.argsort(all_fitness_values)[::-1][:len(mutated_offspring)]):
            population[idx] = mutated_offspring[i]
        
        # Ensure population uniqueness
        unique_population = set(tuple(ind) for ind in population)
        while len(unique_population) < population_size:
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            unique_population.add(tuple(individual))
        population = [list(individual) for individual in unique_population]

    # Print best fitness
    if rank == 0:
        print(f"Generation {generation}: Best calculate_fitness = {current_best_calculate_fitness}")

# Update fitness values for the final population
if rank == 0:
    final_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in population])

    # Output the best solution
    best_idx = np.argmin(final_fitness_values)
    best_solution = population[best_idx]
    print("Best Solution:", best_solution)
    print("Total Distance:", calculate_fitness(best_solution, distance_matrix))

end_time = time.time()
elapsed_time = end_time - start_time
if rank == 0:
    print(f"Execution time: {elapsed_time:.2f} seconds")
