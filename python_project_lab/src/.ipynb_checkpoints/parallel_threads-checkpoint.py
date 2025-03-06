import time
from src.functions import parallel_sum_threaded

def run_threads(n, num_threads):
    # Measure execution time for threaded approach
    start_time = time.time()
    sum_result_threaded = parallel_sum_threaded(n, num_threads)
    end_time = time.time()

    execution_time_threaded = end_time - start_time

    print(f"Threaded Sum: {sum_result_threaded}")
    print(f"Execution Time (Threaded): {execution_time_threaded} seconds")
