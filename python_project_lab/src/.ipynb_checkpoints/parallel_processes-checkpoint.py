import time
from functions import parallel_sum_multiprocessing

# Measure execution time for multiprocessing approach
num_processes = 4
start_time = time.time()
sum_result_multiprocessing = parallel_sum_multiprocessing(n, num_processes)
end_time = time.time()

execution_time_multiprocessing = end_time - start_time

print(f"Multiprocessing Sum: {sum_result_multiprocessing}")
print(f"Execution Time (Multiprocessing): {execution_time_multiprocessing} seconds")
