import os
import time
from src.utils import latest_temperatures, temperature_averages, lock

def initialize_display():
    """Prints the initial layout for temperature monitoring."""
    print("Current temperatures:\n")
    print(f"Latest Temperatures: Sensor 0: {latest_temperatures[0]}°C  Sensor 1: {latest_temperatures[1]}°C  Sensor 2: {latest_temperatures[2]}°C")
    for i in range(3):
        print(f"Sensor {i} Average: {temperature_averages[i]}°C")
    print("\nUpdating every 5 seconds...\n")

def update_display():
    """Refreshes temperature display every 5 seconds."""
    initialize_display()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        with lock:
            print("Current temperatures:\n")
            print(f"Latest Temperatures: Sensor 0: {latest_temperatures[0]}°C  Sensor 1: {latest_temperatures[1]}°C  Sensor 2: {latest_temperatures[2]}°C")
            for i in range(3):
                print(f"Sensor {i} Average: {temperature_averages[i]}°C")
        time.sleep(5)