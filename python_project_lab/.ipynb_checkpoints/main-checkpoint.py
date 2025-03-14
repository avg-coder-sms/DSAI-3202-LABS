import multiprocessing
import concurrent.futures
import random
import time
from src.square_compute import *
from src.connection_pool import run_connection_pool_test

def benchmark(func, numbers):
    start = time.time()
    result = func(numbers)
    end = time.time()
    return result, end - start

if __name__ == "__main__":
    size = 10**6  # Change to 10**7 for second test
    numbers = generate_numbers(size)
    
    print("Running square computation benchmarks...")
    
    _, seq_time = benchmark(sequential_squares, numbers)
    _, mp_time = benchmark(multiprocessing_squares, numbers)
    _, pool_map_time = benchmark(pool_map_squares, numbers)
    _, pool_apply_time = benchmark(pool_apply_squares, numbers)
    _, conc_time = benchmark(concurrent_squares, numbers)
    
    print(f"Sequential execution time: {seq_time:.4f} sec")
    print(f"Multiprocessing (individual processes) execution time: {mp_time:.4f} sec")
    print(f"Multiprocessing Pool (map) execution time: {pool_map_time:.4f} sec")
    print(f"Multiprocessing Pool (apply) execution time: {pool_apply_time:.4f} sec")
    print(f"Concurrent.futures execution time: {conc_time:.4f} sec")
    
    print("\nRunning ConnectionPool test...")
    run_connection_pool_test()
