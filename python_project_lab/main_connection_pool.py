import multiprocessing
from src.connection_pool.connection_pool import ConnectionPool
from src.connection_pool.db_access import access_database

if __name__ == "__main__":
    max_connections = 3
    num_processes = 6  # More processes than available connections
    pool = ConnectionPool(max_connections)

    processes = []
    for i in range(num_processes):
        p = multiprocessing.Process(target=access_database, args=(pool, i))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("All processes completed.")
