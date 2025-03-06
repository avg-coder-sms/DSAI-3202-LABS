import time
from sensor import latest_temperatures
from processor import temperature_averages
from threading import RLock

lock = RLock()

def initialize_display():
    print("Current temperatures:")
    print("Latest Temperatures: ", end="")
    for i in range(3):
        print(f"Sensor {i}: --°C", end=" ")
    print("\nAverages: --°C")

def update_display():
    while True:
        with lock:
            temp_str = " ".join([f"Sensor {i}: {latest_temperatures.get(i, '--')}°C" for i in range(3)])
            avg_temp = temperature_averages.get('average', '--')
            print(f"\rLatest Temperatures: {temp_str} | Average: {avg_temp:.2f}°C", end="")
        time.sleep(5)  # Update every 5 seconds
