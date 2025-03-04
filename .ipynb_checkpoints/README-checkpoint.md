# Lab 3 Part 1: Data Parallel Model  

Parallel and distributed computing enhances computational efficiency by enabling tasks to run concurrently. This lab focuses on implementing a **data parallel model** using both **threads** and **processes** in Python.  

The lab consists of three main implementations:  

1. **Sequential Execution** – Computes the sum of all numbers from 1 to a large given number and measures execution time.  
2. **Threading** – Divides the summation task into multiple threads, each handling a portion of the range, and measures performance improvements.  
3. **Multiprocessing** – Uses separate processes instead of threads to compute partial sums in parallel, comparing execution times with the previous implementations.  

To analyze performance, execution time will be measured for each case, and key performance metrics such as **speedup**, **efficiency**, and theoretical models (**Amdahl’s Law & Gustafson’s Law**) will be applied. The lab also explores the differences between threading and multiprocessing, discussing challenges and best practices for parallel programming.  


# Lab 3 Part 2: Data Parallel Model  

## Introduction  

This part of the lab focuses on enhancing the training of a machine learning model through parallelism, specifically by leveraging **threading** and **multiprocessing**. The goal is to optimize the time taken for hyperparameter tuning using parallel computation techniques.  

The lab tasks include:  

1. **Data Preparation** – Downloading the required files, transferring them to a remote machine, and organizing the data and notebook files for further analysis.  
2. **Testing the Machine Learning Program** – Setting up the environment and testing an initial machine learning model to ensure it works correctly.  
3. **Sequential Search for Best Parameters** – Running the hyperparameter search sequentially and measuring execution time.  
4. **Parallelizing with Threading and Multiprocessing** – Modifying the program to use both **threading** and **multiprocessing** modules to parallelize the hyperparameter search.  
5. **Performance Metrics** – Analyzing the changes in execution time and computing performance metrics for both threading and multiprocessing approaches.  

The objective is to compare how different parallelization techniques impact the overall execution time and assess which method is more efficient in the context of machine learning tasks.
