-- Database schema for IoT sensor monitoring system
-- Time-series data with intentional missing indexes

CREATE TABLE sensors (
    sensor_id VARCHAR(50) PRIMARY KEY,
    device_type VARCHAR(100) NOT NULL,
    location_zone VARCHAR(50),
    installation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    firmware_version VARCHAR(20),
    status VARCHAR(20)
);

CREATE TABLE sensor_readings (
    reading_id INTEGER PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperature_celsius DECIMAL(5, 2),
    humidity_percent DECIMAL(5, 2),
    pressure_hpa DECIMAL(7, 2),
    battery_level INTEGER,
    signal_strength INTEGER,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
);

CREATE TABLE alert_rules (
    rule_id INTEGER PRIMARY KEY,
    sensor_id VARCHAR(50),
    metric_name VARCHAR(50) NOT NULL,
    threshold_value DECIMAL(10, 2),
    comparison_operator VARCHAR(10),
    severity VARCHAR(20),
    enabled BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
);

CREATE TABLE alert_history (
    alert_id INTEGER PRIMARY KEY,
    rule_id INTEGER NOT NULL,
    sensor_id VARCHAR(50) NOT NULL,
    triggered_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    actual_value DECIMAL(10, 2),
    acknowledged BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (rule_id) REFERENCES alert_rules(rule_id),
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
);

CREATE TABLE maintenance_logs (
    log_id INTEGER PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    maintenance_date TIMESTAMP NOT NULL,
    technician_id VARCHAR(50),
    maintenance_type VARCHAR(50),
    notes TEXT,
    next_maintenance_due TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
);

-- Indexes that DO exist (for reference)
CREATE INDEX idx_readings_sensor_id ON sensor_readings(sensor_id);
CREATE INDEX idx_alert_history_rule_id ON alert_history(rule_id);
