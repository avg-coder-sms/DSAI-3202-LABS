import threading
import multiprocessing

# Function to calculate the sum from 1 to n
def sequential_sum(n):
    return sum(range(1, n+1))

# Function to calculate the sum of a specific range
def thread_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))

# Function to calculate the sum in parallel using threading
def parallel_sum_threaded(n, num_threads):
    threads = []
    result = [0] * num_threads
    range_size = n // num_threads

    # Create threads for different parts of the range
    for i in range(num_threads):
        start = i * range_size + 1
        end = (i + 1) * range_size if i != num_threads - 1 else n
        thread = threading.Thread(target=thread_sum, args=(start, end, result, i))
        threads.append(thread)
        thread.start()

    # Join all threads
    for thread in threads:
        thread.join()

    return sum(result)

# Function to calculate the sum of a specific range (for multiprocessing)
def process_sum(start, end):
    return sum(range(start, end + 1))

# Function to calculate the sum in parallel using multiprocessing
def parallel_sum_multiprocessing(n, num_processes):
    pool = multiprocessing.Pool(processes=num_processes)
    range_size = n // num_processes
    ranges = [(i * range_size + 1, (i + 1) * range_size if i != num_processes - 1 else n) for i in range(num_processes)]

    # Compute the sums in parallel
    results = pool.starmap(process_sum, ranges)

    return sum(results)
