import multiprocessing
import time

class ConnectionPool:
    """Manages a limited number of database connections using a semaphore."""

    def __init__(self, max_connections=3):
        self.semaphore = multiprocessing.Semaphore(max_connections)
        self.connections = [f"Connection-{i}" for i in range(max_connections)]

    def get_connection(self):
        """Acquire a connection from the pool."""
        self.semaphore.acquire()
        return self.connections.pop()

    def release_connection(self, connection):
        """Release a connection back to the pool."""
        self.connections.append(connection)
        self.semaphore.release()
