import multiprocessing
import time
import random

class ConnectionPool:
    def __init__(self, max_connections):
        self.semaphore = multiprocessing.Semaphore(max_connections)
        self.connections = [f"Connection-{i}" for i in range(max_connections)]

    def get_connection(self):
        self.semaphore.acquire()
        return self.connections.pop()

    def release_connection(self, conn):
        self.connections.append(conn)
        self.semaphore.release()

def access_database(pool):
    conn = pool.get_connection()
    print(f"{multiprocessing.current_process().name} acquired {conn}")
    time.sleep(random.uniform(0.5, 2.0))  # Simulate a database operation
    pool.release_connection(conn)
    print(f"{multiprocessing.current_process().name} released {conn}")

def run_connection_pool_test():
    pool = ConnectionPool(max_connections=3)
    processes = []

    for _ in range(5):  # More processes than available connections
        p = multiprocessing.Process(target=access_database, args=(pool,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    run_connection_pool_test()
