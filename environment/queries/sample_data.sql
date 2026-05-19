-- Sample data for testing queries

INSERT INTO sensors (sensor_id, device_type, location_zone, firmware_version, status) VALUES
('SN-001', 'temperature', 'Zone-A', 'v2.1.0', 'active'),
('SN-045', 'humidity', 'Zone-B', 'v2.0.5', 'active'),
('SN-100', 'pressure', 'Zone-A', 'v2.1.0', 'active');

INSERT INTO sensor_readings (reading_id, sensor_id, timestamp, temperature_celsius, humidity_percent, pressure_hpa, battery_level, signal_strength) VALUES
(1, 'SN-001', '2024-01-15 10:30:00', 22.5, 45.2, 1013.25, 85, -65),
(2, 'SN-001', '2024-01-15 11:00:00', 23.1, 46.0, 1013.30, 84, -66),
(3, 'SN-045', '2024-01-15 10:30:00', 21.8, 48.5, 1013.20, 92, -58);

INSERT INTO alert_rules (rule_id, sensor_id, metric_name, threshold_value, comparison_operator, severity, enabled) VALUES
(1, 'SN-001', 'temperature_celsius', 30.0, '>', 'high', TRUE),
(2, 'SN-045', 'humidity_percent', 80.0, '>', 'medium', TRUE);

INSERT INTO alert_history (alert_id, rule_id, sensor_id, triggered_at, resolved_at, actual_value, acknowledged) VALUES
(1, 1, 'SN-001', '2024-01-15 14:00:00', '2024-01-15 14:30:00', 31.2, TRUE),
(2, 2, 'SN-045', '2024-01-16 09:00:00', NULL, 82.5, FALSE);

INSERT INTO maintenance_logs (log_id, sensor_id, maintenance_date, technician_id, maintenance_type, notes, next_maintenance_due) VALUES
(1, 'SN-001', '2024-01-10 08:00:00', 'TECH-001', 'calibration', 'Sensor recalibrated', '2024-04-10 08:00:00'),
(2, 'SN-045', '2024-01-12 10:00:00', 'TECH-002', 'battery_replace', 'Battery replaced', '2024-07-12 10:00:00');
