import time
from functions import sequential_sum

# Input for large number
n = 10000000

# Measure execution time
start_time = time.time()
sum_result = sequential_sum(n)
end_time = time.time()

execution_time = end_time - start_time

print(f"Sequential Sum: {sum_result}")
print(f"Execution Time: {execution_time} seconds")

