from mpi4py import MPI
import numpy as np
import time

# Define the square function
def square_numbers(start, end):
    return [i ** 2 for i in range(start, end)]

def main():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    n = int(1e8)  # Adjust this value as needed for different sizes
    # Split the work: each process will handle a subset of the range
    chunk_size = n // size
    
    start_index = rank * chunk_size + 1
    end_index = (rank + 1) * chunk_size + 1 if rank != size - 1 else n + 1
    
    # Calculate squares in parallel
    local_squares = square_numbers(start_index, end_index)
    
    # Gather all results at the root process
    all_squares = comm.gather(local_squares, root=0)
    
    # Only rank 0 will print the final result
    if rank == 0:
        # Flatten the list of lists into a single list
        final_squares = [square for sublist in all_squares for square in sublist]
        print(f"Total number of squares computed: {len(final_squares)}")
        print(f"The last square: {final_squares[-1]}")
        print(f"Time taken: {time.time() - start_time:.4f} seconds")

if __name__ == "__main__":
    start_time = time.time()  # Start time measurement
    main()
