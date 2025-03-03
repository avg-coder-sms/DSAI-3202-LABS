# Questions

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

