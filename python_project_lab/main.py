from src.sequential import run_sequential
from src.parallel_threads import run_threads
from src.parallel_processes import run_processes
import time

def performance_analysis(n):
    num_threads = 4  
    num_processes = 4  
    P = 0.9  

    print("\nRunning Sequential Execution...")
    start = time.perf_counter()
    run_sequential(n)
    T_sequential = time.perf_counter() - start

    print("\nRunning Threading Execution...")
    start = time.perf_counter()
    run_threads(n, num_threads)
    T_threads = time.perf_counter() - start

    print("\nRunning Multiprocessing Execution...")
    start = time.perf_counter()
    run_processes(n, num_processes)
    T_processes = time.perf_counter() - start

    # Compute Speedups
    S_threads = T_sequential / T_threads
    S_processes = T_sequential / T_processes

    # Compute Efficiencies
    E_threads = S_threads / num_threads
    E_processes = S_processes / num_processes

    # Compute Amdahl’s Speedup
    S_A_threads = 1 / ((1 - P) + (P / num_threads))
    S_A_processes = 1 / ((1 - P) + (P / num_processes))

    # Compute Gustafson’s Speedup
    S_G_threads = (1 - P) + (P * num_threads)
    S_G_processes = (1 - P) + (P * num_processes)

    print("\n=== Performance Analysis Results ===")
    print(f"Sequential Time: {T_sequential:.6f} sec")
    print(f"Threading Time: {T_threads:.6f} sec, Speedup: {S_threads:.2f}, Efficiency: {E_threads:.2f}")
    print(f"Multiprocessing Time: {T_processes:.6f} sec, Speedup: {S_processes:.2f}, Efficiency: {E_processes:.2f}")
    print(f"Amdahl’s Law Speedup (Threads): {S_A_threads:.2f}")
    print(f"Amdahl’s Law Speedup (Processes): {S_A_processes:.2f}")
    print(f"Gustafson’s Law Speedup (Threads): {S_G_threads:.2f}")
    print(f"Gustafson’s Law Speedup (Processes): {S_G_processes:.2f}")

# Run tasks
N = 10**7  # 10 million for faster benchmarking

print("task 3_a: sequential")
run_sequential(N)

print("\ntask 3_b: Parallelize with Threading")
run_threads(N, 4)

print("\ntask 3_c: Parallelize with Multiprocessing")
run_processes(N, 4)

print("\ntask 3_d: Performance analysis")
performance_analysis(N)
