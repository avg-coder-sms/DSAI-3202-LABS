# Step 5.d: Explain and Run the Algorithm


## 📝 Explanation of `genetic_algorithm_trial.py`

This script **executes the genetic algorithm** using the functions defined in `genetic_algorithms_functions.py`. Below is an outline of its working:

### **1️⃣ Load the Distance Matrix**
```python
import pandas as pd
distance_matrix = pd.read_csv('./data/city_distances.csv', header=None).to_numpy()
```
- Loads the distance matrix from `city_distances.csv`.
- Converts it into a **NumPy array** for efficient computation.

### **2️⃣ Initialize the Population**
```python
population = generate_valid_population(distance_matrix, population_size=100, num_nodes=32)
```
- A **population of routes** is randomly generated.
- Each route must **start and end at the depot (node 0)**.
- Only **valid routes** (no `100000` distances) are included.

### **3️⃣ Genetic Algorithm Iterations**
```python
for generation in range(num_generations):
    fitness_scores = np.array([calculate_fitness(route, distance_matrix) for route in population])
    selected_parents = select_in_tournament(population, fitness_scores)
```
- Runs for a **fixed number of generations**.
- **Evaluates fitness** for each route using `calculate_fitness()`.
- **Selects parents** for reproduction using **tournament selection**.

### **4️⃣ Crossover & Mutation**
```python
offspring = [mutate(order_crossover(selected_parents[i], selected_parents[i+1])) 
             for i in range(0, len(selected_parents), 2)]
```
- Applies **crossover** (mixes genes from parents).
- Applies **mutation** (random changes to routes).
- Ensures **diversity** in the population.

### **5️⃣ Update Population**
```python
population = offspring
```
- The **new generation replaces** the old population.
- Process repeats until the **termination condition** is met.

### **6️⃣ Get the Best Solution**
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
Best Solution: [0, 5, 12, 8, 3, 7, 6, 10, 9, 2, 1, 4, 0]
Total Distance: -152.3
Execution Time: 8.15 seconds
```