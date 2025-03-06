# Temperature Monitoring System  

## **1. Synchronization Metrics Used**  

The following synchronization techniques were applied in different parts of the project to ensure thread safety and proper data flow:  

| **Task**                            | **Synchronization Metric Used** | **Reason** |
|--------------------------------------|--------------------------------|------------|
| Simulating sensor readings (`simulate_sensor`) | `RLock` (Reentrant Lock) | Ensures that multiple sensors can safely update the shared `latest_temperatures` dictionary without conflicts. |
| Processing temperature data (`process_temperatures`) | `Condition` (with a `Queue`) | Used to synchronize temperature calculations, ensuring the processor waits for new sensor data before computing averages. |
| Displaying real-time updates (`update_display`) | `RLock` | Prevents race conditions while accessing shared dictionaries (`latest_temperatures` and `temperature_averages`). |
| Managing data transfer (`Queue`) | `Queue` (thread-safe structure) | Used for safe communication between the sensor threads and the processor thread. |

## **2. Why Did the Professor Not Ask to Compute Metrics?**  

The professor likely did not require explicit metric computation (e.g., performance benchmarks) because:  

1. **Focus on Thread Synchronization**  
   - The primary goal of the assignment is to apply synchronization concepts (`RLock`, `Condition`, and `Queue`), rather than measure execution speed or resource usage.  

2. **Predictable Execution Patterns**  
   - Since sensor readings and processing occur at predefined intervals (1s for readings, 5s for display updates), performance analysis is less critical.  

3. **Introductory Nature of the Task**  
   - The assignment focuses on understanding **concurrent programming** in Python rather than optimizing execution time or memory usage.  

4. **No High-Performance Requirement**  
   - The system is relatively lightweight, meaning advanced metrics like execution time or CPU utilization would not provide significant insights.  

