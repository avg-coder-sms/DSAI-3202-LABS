import time
from src.sequential import run_sequential
from src.parallel import run_parallel

def main():
    # Run the sequential and parallel tasks
    run_sequential()
    run_parallel()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    total_execution_time = end_time - start_time
    print(f"Total execution time for both sequential and parallel runs: {total_execution_time} seconds.")
