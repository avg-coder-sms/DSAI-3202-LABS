import time
from src.functions import generate_and_join_letters
from src.functions import generate_and_add_numbers

def run_sequential():
    print("Starting the Program")
    total_start_time = time.time()

    generate_and_add_numbers(int(1e7))
    generate_and_join_letters(int(1e7))

    total_end_time = time.time()
    print("Exiting the Program")
    sequential_execution_time = total_end_time - total_start_time
    print(f"It took {sequential_execution_time}s to execute the tasks.")
