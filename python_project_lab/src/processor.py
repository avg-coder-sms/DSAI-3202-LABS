import threading

temperature_averages = {}
condition = threading.Condition()

def process_temperatures(temp_queue, condition):
    while True:
        with condition:
            condition.wait()  # Wait for a new temperature to be available
            temps = list(temp_queue.queue)
            if temps:
                avg_temp = sum(temps) / len(temps)
                temperature_averages['average'] = avg_temp
                temp_queue.queue.clear()  # Clear processed data

