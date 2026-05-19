-- Q1: Find sensors by location zone for dashboard
SELECT * FROM sensors WHERE location_zone = 'Zone-A';

-- Q2: Get temperature readings for a sensor with device details
SELECT * FROM sensor_readings r 
JOIN sensors s ON r.sensor_id = s.sensor_id 
WHERE s.device_type = 'temperature' 
AND r.timestamp >= '2024-01-01';

-- Q3: Find recent alerts for critical sensors
SELECT * FROM alert_history 
WHERE triggered_at >= '2024-01-15' 
AND triggered_at < '2024-01-16';

-- Q4: Get sensor readings with alert history and maintenance logs
SELECT * FROM sensors s
JOIN sensor_readings r ON s.sensor_id = r.sensor_id
JOIN alert_history a ON s.sensor_id = a.sensor_id
JOIN maintenance_logs m ON s.sensor_id = m.sensor_id
WHERE s.sensor_id = 'SN-045';

-- Q5: Find sensors with low battery using function
SELECT * FROM sensors 
WHERE LOWER(device_type) LIKE '%temp%';

-- Q6: Get recent readings for a sensor ordered by timestamp
SELECT * FROM sensor_readings 
WHERE sensor_id = 'SN-100' 
ORDER BY timestamp DESC;
