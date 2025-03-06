import threading
import random
import time
from queue import Queue

# Global data structure
latest_temperatures = {}
lock = threading.RLock()

def simulate_sensor(sensor_id, temp_queue, condition):
    while True:
        temp = random.randint(15, 40)
        with lock:
            latest_temperatures[sensor_id] = temp
        temp_queue.put(temp)
        with condition:
            condition.notify()  # Notify processor when a new temperature is added
        time.sleep(1)

