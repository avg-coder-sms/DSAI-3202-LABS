import multiprocessing
import concurrent.futures
import random

def square(n):
    return n * n

def generate_numbers(size):
    return [random.randint(1, 100) for _ in range(size)]

def sequential_squares(numbers):
    return [square(n) for n in numbers]

def multiprocessing_squares(numbers):
    processes = []
    results = multiprocessing.Manager().list()
    
    def collect_result(num):
        results.append(square(num))

    for num in numbers:
        p = multiprocessing.Process(target=collect_result, args=(num,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return list(results)

def pool_map_squares(numbers):
    with multiprocessing.Pool() as pool:
        return pool.map(square, numbers)

def pool_apply_squares(numbers):
    with multiprocessing.Pool() as pool:
        results = [pool.apply(square, args=(n,)) for n in numbers]
    return results

def concurrent_squares(numbers):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        return list(executor.map(square, numbers))
