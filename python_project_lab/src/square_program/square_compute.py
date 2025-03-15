import multiprocessing
import concurrent.futures
import random

def square(n):
    """Computes the square of a number."""
    return n * n

def generate_numbers(size):
    """Generates a list of random numbers."""
    return [random.randint(1, 100) for _ in range(size)]

def sequential_squares(numbers):
    """Computes squares sequentially using a for loop."""
    return [square(n) for n in numbers]

def multiprocessing_squares(numbers):
    """Computes squares using individual multiprocessing processes."""
    processes = []
    results = multiprocessing.Manager().list()

    def compute_square(num):
        results.append(square(num))

    for num in numbers:
        p = multiprocessing.Process(target=compute_square, args=(num,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return list(results)

def pool_map_squares(numbers):
    """Computes squares using multiprocessing Pool with map()."""
    with multiprocessing.Pool() as pool:
        return pool.map(square, numbers)

def pool_map_async_squares(numbers):
    """Computes squares asynchronously using multiprocessing Pool with map_async()."""
    with multiprocessing.Pool() as pool:
        result = pool.map_async(square, numbers)
        return result.get()  # Wait for results

def pool_apply_squares(numbers):
    """Computes squares using multiprocessing Pool with apply()."""
    with multiprocessing.Pool() as pool:
        results = [pool.apply(square, args=(n,)) for n in numbers]
    return results

def pool_apply_async_squares(numbers):
    """Computes squares asynchronously using multiprocessing Pool with apply_async()."""
    with multiprocessing.Pool() as pool:
        results = [pool.apply_async(square, args=(n,)) for n in numbers]
        return [r.get() for r in results]  # Wait for each result

def concurrent_squares(numbers):
    """Computes squares using concurrent.futures ProcessPoolExecutor."""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        return list(executor.map(square, numbers))
