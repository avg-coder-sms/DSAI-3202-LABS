# Lab 3 Part 1: Data Parallel Model  

Parallel and distributed computing enhances computational efficiency by enabling tasks to run concurrently. This lab focuses on implementing a **data parallel model** using both **threads** and **processes** in Python.  

The lab consists of three main implementations:  

1. **Sequential Execution** – Computes the sum of all numbers from 1 to a large given number and measures execution time.  
2. **Threading** – Divides the summation task into multiple threads, each handling a portion of the range, and measures performance improvements.  
3. **Multiprocessing** – Uses separate processes instead of threads to compute partial sums in parallel, comparing execution times with the previous implementations.  

To analyze performance, execution time will be measured for each case, and key performance metrics such as **speedup**, **efficiency**, and theoretical models (**Amdahl’s Law & Gustafson’s Law**) will be applied. The lab also explores the differences between threading and multiprocessing, discussing challenges and best practices for parallel programming.  
