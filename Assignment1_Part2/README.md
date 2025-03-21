# Step 5.d: Explain and Run the Algorithm


## Explanation of `genetic_algorithm_trial.py`

This script **executes the genetic algorithm** using the functions defined in `genetic_algorithms_functions.py`. Below is an outline of its working:

### **1 Load the Distance Matrix**
```python
import pandas as pd
distance_matrix = pd.read_csv('./data/city_distances.csv', header=None).to_numpy()
```
- Loads the distance matrix from `city_distances.csv`.
- Converts it into a **NumPy array** for efficient computation.

### **2 Initialize the Population**
```python
population = generate_valid_population(distance_matrix, population_size=100, num_nodes=32)
```
- A **population of routes** is randomly generated.
- Each route must **start and end at the depot (node 0)**.
- Only **valid routes** (no `100000` distances) are included.

### **3 Genetic Algorithm Iterations**
```python
for generation in range(num_generations):
    fitness_scores = np.array([calculate_fitness(route, distance_matrix) for route in population])
    selected_parents = select_in_tournament(population, fitness_scores)
```
- Runs for a **fixed number of generations**.
- **Evaluates fitness** for each route using `calculate_fitness()`.
- **Selects parents** for reproduction using **tournament selection**.

### **4 Crossover & Mutation**
```python
offspring = [mutate(order_crossover(selected_parents[i], selected_parents[i+1])) 
             for i in range(0, len(selected_parents), 2)]
```
- Applies **crossover** (mixes genes from parents).
- Applies **mutation** (random changes to routes).
- Ensures **diversity** in the population.

### **5 Update Population**
```python
population = offspring
```
- The **new generation replaces** the old population.
- Process repeats until the **termination condition** is met.

### **6 Get the Best Solution**
```python
best_idx = np.argmax(fitness_scores)
best_route = population[best_idx]
print(f"Best Solution: {best_route}")
print(f"Total Distance: {fitness_scores[best_idx]}")
```
- The **best route** is selected from the final population.
- The **total distance** of the best route is displayed.

---


## Output
```
Best Solution: [0, 12, 7, 15, 18, 31, 28, 5, 3, 6, 9, 23, 22, 20, 1, 2, 10, 25, 13, 29, 11, 30, 8, 21, 4, 19, 14, 26, 17, 27, 16, 24]
Total Distance: -1800505.0
Execution time: 19.60 seconds
```




# 6.Parallelization of Genetic Algorithm using MPI

## Parts to be Distributed and Parallelized

### 1. Fitness Calculation  
- Each individual in the population requires an independent fitness evaluation.  
- **Reason for parallelization**: Each fitness calculation is independent, so parallelizing this step will significantly improve performance.  

### 2. Tournament Selection  
- The tournament selection process can run multiple tournaments concurrently.  
- **Reason for parallelization**: Each tournament selection is independent, reducing computation time.  

### 3. Crossover and Mutation  
- The crossover and mutation operations on selected individuals are independent.  
- **Reason for parallelization**: Parallelizing these steps speeds up offspring generation.  

### 4. Population Regeneration  
- When stagnation occurs, a new population needs to be generated.  
- **Reason for parallelization**: The regeneration process does not require sequential execution.  

---

## Parallelization Strategy  

- Use `mpi4py` to distribute computations across multiple machines.  
- Each machine will handle a portion of the population.  
- Key parallelized tasks:
  - Fitness calculation
  - Tournament selection
  - Crossover and mutation
  - Population regeneration

---

## Parallelized Code Implementation  

```python
from mpi4py import MPI
import numpy as np
import pandas as pd
from genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, \
    generate_unique_population, generate_valid_population
import time

# MPI Setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Load the distance matrix
if rank == 0:
    distance_matrix = pd.read_csv('/home/student/DSAI-3202-LABS/Assignment1_Part2/data/city_distances.csv').to_numpy()

# Broadcast the distance matrix to all processes
distance_matrix = comm.bcast(distance_matrix, root=0)

# Parameters
num_nodes = distance_matrix.shape[0]
population_size = 10000
mutation_rate = 0.1
num_generations = 200
stagnation_limit = 5

# Generate initial population
np.random.seed(42)
population = generate_unique_population(population_size, num_nodes)

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
```

---

## Explanation of Changes  

### **1. MPI Setup**  
- `comm = MPI.COMM_WORLD`: Initializes communication between processes.  
- `rank = comm.Get_rank()`: Gets process rank.  
- `size = comm.Get_size()`: Gets the number of processes.  

### **2. Broadcasting Distance Matrix**  
- The root process (rank 0) loads the distance matrix and broadcasts it to all other processes.  

### **3. Parallel Fitness Calculation**  
- Each process calculates fitness for a chunk of the population.  
- Results are gathered at rank 0 for selection and crossover.  

### **4. Selection, Crossover, and Mutation on Rank 0**  
- Rank 0 selects parents, performs crossover and mutation.  
- Ensures population uniqueness.  

### **5. Performance Metrics**  
- Execution time is measured and printed by rank 0.  
- Output: 
Best Solution: [0, 27, 20, 12, 30, 3, 14, 26, 22, 31, 18, 19, 21, 25, 29, 16, 10, 28, 15, 6, 13, 24, 8, 9, 5, 2, 1, 4, 17, 11, 23, 7]
Total Distance: -1600910.0
Execution time: 8.85 seconds
---

## Performance Evaluation  

### **1. Speedup**  
- S = Ts/Tp
    = 19.60/8.85
    =2.2

### **2. Efficiency**  
- E = S/np
    = 2.2/4
    =0.55

---

## Running the Parallel Code  

To execute on multiple machines:  

```bash
mpirun -n 4 python3 parallel_genetic_algorithm.py
```
# 7 Enhancements

## **1. Parallelized Fitness Evaluation using MPI**
### **Why?**  
In the original sequential implementation, fitness evaluation was performed for each individual in the population one by one, making it the most computationally expensive step. By using **MPI (Message Passing Interface)**, we distribute this computation across multiple machines to significantly reduce execution time.

### **How?**  
- The fitness evaluation step:  
  ```python
  calculate_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in population])
  ```
  is parallelized by distributing chunks of the population across different machines, allowing each machine to process fitness calculations independently.

- **MPI Code Snippet:**
  ```python
  from mpi4py import MPI
  
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  size = comm.Get_size()

  chunk_size = len(population) // size
  local_population = population[rank * chunk_size:(rank + 1) * chunk_size]

  local_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in local_population])

  # Gather results at the root process
  global_fitness_values = np.zeros(len(population))
  comm.Gather(local_fitness_values, global_fitness_values, root=0)
  ```

- This allows each machine to compute fitness for a subset of the population, reducing total computation time.

---

## **2. Elitism Strategy to Preserve the Best Solution**
### **Why?**  
In genetic algorithms, **elitism** ensures that the best solution from one generation is carried forward to the next, preventing loss of the best-found solutions due to crossover or mutation.

### **How?**  
- Before replacement, we store the best individual:
  ```python
  best_idx = np.argmin(calculate_fitness_values)
  best_individual = population[best_idx]
  ```
- The best individual is **always preserved**:
  ```python
  new_population[0] = best_individual  # Keep the best solution in the next generation
  ```

- This prevents **good solutions from being lost**, ensuring steady improvement across generations.

---

## **3. Adaptive Mutation Rate for Escaping Local Minima**
### **Why?**  
A fixed mutation rate can make the algorithm **too rigid**—either converging too early (if too low) or causing excessive randomness (if too high). An **adaptive mutation rate** adjusts based on **stagnation** (when the best fitness hasn’t improved for multiple generations).

### **How?**  
- The mutation rate **increases** if the best solution has stagnated:
  ```python
  if stagnation_counter >= stagnation_limit:
      mutation_rate *= 1.5  # Increase mutation rate to escape local minima
  else:
      mutation_rate = max(0.1, mutation_rate * 0.95)  # Decay mutation rate slightly
  ```
- This helps the algorithm explore new solutions dynamically.

---

## **4. Dynamic Load Balancing for Even Work Distribution**
### **Why?**  
When distributing computations across machines, some processes may complete faster than others due to **uneven workload distribution**. This leads to inefficiencies where some machines are idle while others are still computing.

### **How?**  
- Instead of static partitioning, **dynamic load balancing** ensures machines request new tasks **as they complete previous ones**.
- Implemented with MPI’s **scatter-gather approach**:
  ```python
  while not all_tasks_completed:
      local_population = comm.scatter(population_chunks, root=0)
      local_results = [calculate_fitness(route, distance_matrix) for route in local_population]
      comm.gather(local_results, root=0)
  ```
- This keeps all machines busy **at all times**, improving efficiency.


## **5. Distributed Execution with MPI for Multi-Machine Scaling**
### **Why?**  
By distributing the algorithm over multiple machines, we **significantly reduce execution time** while handling larger populations.

### **How?**  
- Machines are specified in `hosts.txt`
- Running with MPI:
- This ensures workload is **evenly divided**.



# **Conclusion**
These enhancements improve the efficiency and robustness of the genetic algorithm by:
1. **Reducing execution time** through parallelization.
2. **Preserving high-quality solutions** with elitism.
3. **Escaping local minima** with adaptive mutation.
4. **Ensuring balanced workload** distribution.
5. **Scaling across multiple machines** using MPI.


## Output
Best Solution: [ 0 12  7 15 18 31 28  5  3  6  9 23 22 20  1  2 10 25 13 29 11 30  8 21
  4 19 14 26 17 27 16 24]
Total Distance: -1800505.0
Parallel Execution Time: 6.69 seconds

## **Performance Comparison**  

| Metric                         | Before Enhancements | After Enhancements |
|--------------------------------|---------------------|--------------------|
| Execution Time (seconds)       | 8.85            | 6.69           |
| Best Fitness Score             | -1600910.0            | -1800505.0           |
| Speedup | 2.2               | 2.93              |
| Efficiency                 | 0.55             | 0.73            |

## Running the Enhanced Parallel Code  

To execute on multiple machines:  

```bash
mpirun -hostfile hosts.txt -n 8 python enhanced_genetic_algorithm.py
```

# 8 Running the Program with Extended City Map 

## Running the Enhanced Parallel Code  

To execute on multiple machines:  

```bash
mpirun -hostfile hosts.txt -n 8 python extended_genetic_algorithm.py
```

## Output

Best Solution: [ 0 65 76 95  1 87  7  6  3 79 43 13 22 81 74 85 20 72 84 39 69 73 36 97
 49 51 77 15 88 66 53 70 83 75  8 98 32 82 24 11 90 56 12 28 14 94 78 31
 50 16 61 46 33 19 60 40 63 91 92 55 52  5 37 18 80 10 99 48 47 42 86 29
  9 41 38 34 45 71 58 26 25 59 67 64 57 62  4 17 93 54 30 35 89  2 21 27
 23 44 96 68]
Total Distance: -3802866.0
Parallel Execution Time: 18.51 seconds

## Adding More Cars to the Problem  

In the current problem, a single car follows a route to visit all cities. To add more cars, we can modify the genetic algorithm as follows:  

1. **Multi-Route Representation**  
   - Instead of a single route, each solution (individual) should encode multiple routes, one per car.  
   - Assign cities to different cars while ensuring all cities are visited once.  

2. **Fitness Function Update**  
   - The fitness function should evaluate the **total travel distance** for all cars instead of just one.  
   - Constraints must be added to balance workload distribution across cars.  

3. **Crossover & Mutation Adjustments**  
   - Crossover should swap city assignments between different cars while maintaining route feasibility.  
   - Mutation should allow reassigning cities between cars to improve overall efficiency.  

4. **Load Balancing Strategy**  
   - A constraint or penalty can be introduced to encourage even distribution of cities among all cars.  
   - Alternatively, a heuristic can optimize assignments to minimize total travel distance.  
