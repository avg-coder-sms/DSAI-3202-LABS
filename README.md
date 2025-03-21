# **DSAI 3202 – Parallel and Distributed Computing Assignment 1 – Part 1/2: Multiprocessing**

## **Introduction**

This assignment focuses on leveraging Python’s multiprocessing capabilities to perform parallel computations and manage resources effectively. The tasks are designed to explore various approaches to parallelization and synchronization, including using Python’s `multiprocessing`, `concurrent.futures`, and semaphores.

### **Square Program**

The first part of the assignment involves implementing a function to compute the square of an integer and timing the execution under different scenarios. These include sequential execution, multiprocessing with a separate process for each number, using a multiprocessing pool, and utilizing the `concurrent.futures.ProcessPoolExecutor`. The goal is to compare the performance of each approach, especially when scaling up the input size from 10^6 to 10^7 numbers. By testing both synchronous and asynchronous versions in the pool, the assignment aims to assess the efficiency and scalability of different parallel computing techniques.

### **Process Synchronization with Semaphores**

The second part involves simulating a limited pool of resources using semaphores to control access to a shared resource. In this case, a `ConnectionPool` class is created to simulate a pool of database connections, with semaphores ensuring that only a limited number of processes can access the pool at any given time. Through this exercise, the assignment introduces the concept of process synchronization and race condition prevention. The program involves creating processes that simulate database operations, where each process must acquire a connection before performing its task and then release it after completion. This part of the assignment demonstrates how semaphores can be used to manage concurrency in a multiprocessing environment.


# **Parallel and Distributed Computing – Assignment 1 (Part 2/2): Navigating the City**

## **Introduction**

This assignment explores the application of genetic algorithms (GAs) for optimizing delivery routes in a city, utilizing parallel and distributed computing techniques. Genetic algorithms are powerful optimization tools inspired by natural selection, and in this project, they are applied to minimize the total distance traveled by a delivery vehicle while ensuring all locations are visited exactly once.

The implementation begins with a sequential version of the algorithm, where a single vehicle navigates a city represented as a graph with nodes and distance constraints. Key genetic algorithm components, including selection, crossover, and mutation, are used to evolve the best route over multiple generations. The core functionality is implemented in Python, leveraging **MPI4PY** for distributed computing.

Following the sequential execution, the project is parallelized to improve computational efficiency. The fitness evaluation and selection processes are distributed across multiple processors, reducing execution time and enabling scalability. The assignment also explores performance metrics, compares sequential and parallel execution times, and extends the problem to a larger city map with 100 nodes.

Further enhancements, including improvements in the selection process and distributed execution over multiple machines, are implemented and analyzed. The report includes a discussion on these optimizations and evaluates the impact on performance and solution quality. Finally, considerations for extending the model to multiple delivery vehicles are discussed, laying the foundation for further scalability and real-world applications.

This project demonstrates the practical use of genetic algorithms in solving optimization problems while highlighting the advantages of parallel and distributed computing in handling complex computational tasks efficiently.
