# Lab3 Part1 Questions

#### How does the execution time change when moving from sequential to threaded to multiprocessing implementations?
- Sequential: Execution time is generally the longest, as it is a single-threaded, single-process computation.
- Threaded: Execution time can be reduced, especially if the task is I/O-bound or if there are multiple cores available. Threading can improve performance by overlapping I/O-bound tasks.
- Multiprocessing: Execution time can be significantly reduced compared to sequential and threaded approaches, especially for CPU-bound tasks. Multiprocessing runs in parallel on multiple CPU cores, which can lead to significant speedup.

#### Calculating speedup
The speedup using threads is 1.239684722692835
The speedup using processes is 2.430130587295523

#### Computing the Efficiency 
The efficiency using threads is 0.30992118067320873
The efficiency using processes is 0.6075326468238808

#### Amdhal and Gustafson Laws
- Amdahl = 2.1052631578947367
- Gustafson = 3.0999999999999996

### Are there any performance differences between the threaded and multiprocessing versions?
Yes, multiprocessing is generally better for CPU-bound tasks, as it avoids Global Interpreter Lock (GIL) limitations in Python, while threading is more suitable for I/O-bound tasks. Threading can provide speedup, but it may be limited by the GIL when working with CPU-intensive operations.

### What challenges did you face when implementing parallelism, and how did you address them?
- Threading GIL: Python’s GIL prevents true parallel execution in threads for CPU-bound tasks. I handled this by using multiprocessing for CPU-heavy tasks.
- Task Division: Dividing the range of numbers efficiently is important for balanced workload across threads or processes. I ensured each thread or process worked on a roughly equal portion of the range.

### When would you choose threading over multiprocessing or vice versa for parallel tasks?
- Threading: Useful for I/O-bound tasks like reading from files or making network requests.
- Multiprocessing: More suitable for CPU-bound tasks, as it avoids the GIL and utilizes multiple cores effectively.

# Lab3 Part2 Questions
### 1) How does the execution time change when moving from sequential to threaded to multiprocessing implementations?

From the times provided:

- **Sequential execution time**: 67.87 seconds
- **Threading execution time**: 26.58 seconds
- **Multiprocessing execution time**: 14.55 seconds

The execution time decreases as we move from sequential to threaded and then to multiprocessing implementations. Here's the breakdown:

- **Sequential to Threaded**: Execution time improves from 67.87 seconds to 26.58 seconds. This reduction occurs because threads allow multiple tasks to be handled concurrently within a single process, optimizing CPU resource usage.
  
- **Threaded to Multiprocessing**: Execution time improves further from 26.58 seconds to 14.55 seconds. This significant reduction happens because multiprocessing utilizes multiple CPU cores, allowing for better parallelization, especially for CPU-bound tasks.

### 2) Compute the performance metrics for the threaded and multiprocessing executions:

To compute the performance metrics, we calculate the following:

1. **Speedup**: The speedup is the ratio of the sequential execution time to the parallel execution time (for threading or multiprocessing), showing how much faster the parallel version is.

   - **Speedup for Threading**:
     \[
     \text{Speedup}_{\text{Threading}} = \frac{\text{Sequential Time}}{\text{Threaded Time}} = \frac{67.87}{26.58} \approx 2.55
     \]
     
   - **Speedup for Multiprocessing**:
     \[
     \text{Speedup}_{\text{Multiprocessing}} = \frac{\text{Sequential Time}}{\text{Multiprocessing Time}} = \frac{67.87}{14.55} \approx 4.66
     \]

2. **Efficiency**: Efficiency is the ratio of the speedup to the number of threads or processes used. We'll assume 4 threads for threading and 4 processes for multiprocessing.

   - **Efficiency for Threading**: Assuming 4 threads:
     \[
     \text{Efficiency}_{\text{Threading}} = \frac{\text{Speedup}_{\text{Threading}}}{\text{Number of Threads}} = \frac{2.55}{4} = 0.6375
     \]

   - **Efficiency for Multiprocessing**: Assuming 4 processes:
     \[
     \text{Efficiency}_{\text{Multiprocessing}} = \frac{\text{Speedup}_{\text{Multiprocessing}}}{\text{Number of Processes}} = \frac{4.66}{4} = 1.165
     \]

### Summary:

- **Threading Speedup**: 2.55
- **Threading Efficiency**: 0.6375 (assuming 4 threads)
- **Multiprocessing Speedup**: 4.66
- **Multiprocessing Efficiency**: 1.165 (assuming 4 processes)

As the number of processes increases in multiprocessing, we see both higher speedup and efficiency compared to threading.

