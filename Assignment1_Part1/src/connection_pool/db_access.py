import multiprocessing
import time
import random

def access_database(pool, process_id):
    """Simulates database access by acquiring and releasing a connection."""
    print(f"Process {process_id} is waiting for a connection...")

    connection = pool.get_connection()
    print(f"Process {process_id} acquired {connection}")

    time.sleep(random.uniform(1, 3))  # Simulate work time

    print(f"Process {process_id} releasing {connection}")
    pool.release_connection(connection)
