
import threading
import time
from queue import Queue
from src.sensor import simulate_sensor
from src.processor import process_temperatures
from src.display import initialize_display, update_display

if __name__ == "__main__":
    temp_queue = Queue()
    condition = threading.Condition()

    initialize_display()

    # Create and start sensor threads
    sensor_threads = [threading.Thread(target=simulate_sensor, args=(i, temp_queue, condition), daemon=True) for i in range(3)]
    for thread in sensor_threads:
        thread.start()

    # Create and start processing thread
    processor_thread = threading.Thread(target=process_temperatures, args=(temp_queue, condition), daemon=True)
    processor_thread.start()
    
    # Create and start display thread
    display_thread = threading.Thread(target=update_display, daemon=True)
    display_thread.start()
    
    while True:
        time.sleep(1)  # Keep main thread alive