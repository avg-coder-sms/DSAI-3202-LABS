# Interpretations
- Computing the speedups

The speedup using threads is 0.9671144381842681
The speedup using processes is 1.8737100431726903

- Computing the Efficiency

The efficiency using threads is 0.24177860954606703
The efficiency using processes is 0.4684275107931726

- Amdhal and Gustafson Laws
Amdahl = 2.9411764705882355
Gustafson = 3.64

# Conclusions

### **Key Takeaways:**

- **Threads**: Threads did not provide much benefit in this case. The speedup was close to 1, and efficiency was low. This suggests that threading may not be the best approach for this particular task or that the overhead of managing threads was high. Threading in Python, especially with the Global Interpreter Lock (GIL), might not always give optimal performance for CPU-bound tasks.

- **Processes**: Processes performed better with a speedup of **1.87** and efficiency of **0.468**, indicating that parallelizing with separate processes (which run in separate memory spaces) can be more effective for tasks that are CPU-bound. This aligns with the observed performance improvement.

- **Amdhal's Law**: The speedup observed using processes is far below the theoretical maximum suggested by Amdhal’s Law (**2.94**), indicating that there are inefficiencies in parallelization. It suggests that further improvements could be made to achieve a speedup closer to the theoretical maximum by reducing overhead or improving parallel workload distribution.

- **Gustafson's Law**: The speedup using Gustafson's Law (**3.64**) suggests that for larger problem sizes, parallelism could lead to even more significant improvements. This indicates that parallelization is more effective for large-scale problems where the workload is substantial enough to benefit from additional processors.

### **Conclusion:**

- **Parallelization with Processes** is more effective than with threads for this specific task, likely due to lower overhead and better CPU utilization with processes.
- **Threading may not always scale well** for CPU-bound tasks in Python, especially when dealing with Python's Global Interpreter Lock (GIL).
- **Amdhal’s Law** provides an upper bound on speedup, which may not always be achievable in real-world scenarios, especially with high overheads or imperfect parallelism.
- **Gustafson’s Law** is more optimistic, showing that parallelization could scale more effectively as the problem size grows, making it more suitable for larger workloads.

Therefore, if you're dealing with larger datasets or more complex tasks, parallelizing with processes is likely to yield better performance. For smaller tasks or workloads, the overhead of parallelism might outweigh the benefits.