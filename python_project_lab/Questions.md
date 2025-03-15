# Remarks for Q3
Running benchmarks for 1000000 numbers...
Sequential execution time: 0.0513 sec
Multiprocessing Pool (map, synchronous) execution time: 0.1106 sec
Multiprocessing Pool (map_async, asynchronous) execution time: 0.1062 sec
Multiprocessing Pool (apply, synchronous) execution time: 166.1157 sec
Multiprocessing Pool (apply_async, asynchronous) execution time: 52.7461 sec
Concurrent.futures execution time: 110.4048 sec


Running benchmarks for 10000000 numbers...
Sequential execution time: 0.5148 sec
Multiprocessing Pool (map, synchronous) execution time: 0.8356 sec
Multiprocessing Pool (map_async, asynchronous) execution time: 0.7684 sec

Multiprocessing Pool (apply_async, asynchronous) execution time: 539.1315 sec





# Observations for Q4
If more processes request a connection than available:

Extra processes will wait until a connection is available.
The semaphore ensures that only max_connections processes can access the database at once.
How the semaphore prevents race conditions:

The acquire() method blocks additional processes until a connection is released.
The release() method returns the connection to the pool, ensuring controlled access.