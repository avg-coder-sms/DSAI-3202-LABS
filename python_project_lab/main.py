import time
from src.square_compute import (
    square, generate_numbers, sequential_squares, multiprocessing_squares, 
    pool_map_squares, pool_apply_squares, concurrent_squares
)

def benchmark(func, numbers):
    """Measures execution time of a function."""
    start = time.time()
    result = func(numbers)
    end = time.time()
    return result, end - start

if __name__ == "__main__":
    for size in [10**6]:  # Testing with 1 million and 10 million numbers
        numbers = generate_numbers(size)
        
        print(f"\nRunning benchmarks for {size} numbers...")

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
