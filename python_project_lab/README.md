# **Remarks for Q3**  

## **Running benchmarks for 1,000,000 numbers**  
```
Sequential execution time: 0.0513 sec  
Multiprocessing Pool (map, synchronous) execution time: 0.1106 sec  
Multiprocessing Pool (map_async, asynchronous) execution time: 0.1062 sec  
Multiprocessing Pool (apply, synchronous) execution time: 166.1157 sec  
Multiprocessing Pool (apply_async, asynchronous) execution time: 52.7461 sec  
Concurrent.futures execution time: 110.4048 sec  
```

## **Running benchmarks for 10,000,000 numbers**  
```
Sequential execution time: 0.5148 sec  
Multiprocessing Pool (map, synchronous) execution time: 0.8356 sec  
Multiprocessing Pool (map_async, asynchronous) execution time: 0.7684 sec  
Multiprocessing Pool (apply_async, asynchronous) execution time: 539.1315 sec  
```

### **Observations**  
- **Multiprocessing Pool (`apply` method, synchronous)** took an extremely long time (**166 sec for 1M numbers**), making it highly inefficient.  
- **Multiprocessing Pool (`apply_async` method, asynchronous)** was faster but still significantly slower than **map-based approaches**.  
- **Concurrent.futures** was also **very slow** compared to `map()`.  
- For **10M numbers**, some benchmarks could not be completed due to insufficient memory.  
- The **apply() method (synchronous)** was skipped for 10M numbers because it was too slow and inefficient.  
- **`map()` and `map_async()`** remained the most efficient approaches.  

---

# **Observations for Q4**  

### **If more processes request a connection than available:**  
- Extra processes will **wait** until a connection is available.  
- The **semaphore** ensures that only `max_connections` processes can access the database at once.  

### **How the semaphore prevents race conditions:**  
- The **`acquire()` method** blocks additional processes **until** a connection is released.  
- The **`release()` method** returns the connection to the pool, ensuring **controlled access**.  