import random
import time
import threading
from src.utils import latest_temperatures, lock

def simulate_sensor(sensor_id):
    """Simulates temperature readings from a sensor every second."""
    while True:
        temp = random.randint(15, 40)
        with lock:
            latest_temperatures[sensor_id] = temp
        time.sleep(1)