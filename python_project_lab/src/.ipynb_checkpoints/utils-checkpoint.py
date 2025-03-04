import threading

# Shared data
latest_temperatures = {0: '--', 1: '--', 2: '--'}
temperature_averages = {0: '--', 1: '--', 2: '--'}

# Synchronization tools
lock = threading.RLock()