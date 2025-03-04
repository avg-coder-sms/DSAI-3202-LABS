import time
from src.utils import latest_temperatures, temperature_averages, lock

def process_temperatures():
    """Computes the average temperature every 5 seconds."""
    while True:
        with lock:
            if latest_temperatures:
                avg_temp = sum(latest_temperatures.values()) / len(latest_temperatures)
                for i in range(3):
                    temperature_averages[i] = avg_temp
        time.sleep(5)