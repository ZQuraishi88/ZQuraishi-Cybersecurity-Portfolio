import re
import json
from datetime import datetime

# Sample function to extract Indicators of Compromise (IOCs) from logs
def extract_iocs(log_data):
    ioc_list = []
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    
    for line in log_data:
        ip_matches = ip_pattern.findall(line)
        url_matches = url_pattern.findall(line)
        if ip_matches:
            ioc_list.extend(ip_matches)
        if url_matches:
            ioc_list.extend(url_matches)
    return list(set(ioc_list))

# Function to parse logs and extract timestamps and alerts
def parse_logs(log_data):
    parsed_logs = []
    for line in log_data:
        if "ALERT" in line:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            parsed_logs.append({"timestamp": timestamp, "alert": line.strip()})
    return parsed_logs

# Function to prioritize alerts based on keywords
def prioritize_alerts(parsed_logs):
    priority_keywords = ["critical", "high", "malware", "breach"]
    prioritized_alerts = []
    
    for log in parsed_logs:
        if any(keyword in log["alert"].lower() for keyword in priority_keywords):
            log["priority"] = "High"
        else:
            log["priority"] = "Low"
        prioritized_alerts.append(log)
    return prioritized_alerts

# Sample log data for testing
log_data = [
    "2024-11-04 ALERT: Suspicious IP detected at 192.168.1.100",
    "2024-11-04 ALERT: Access to malicious URL https://malicious-site.com",
    "2024-11-04 INFO: Routine scan completed successfully",
    "2024-11-04 ALERT: Critical malware detected on endpoint"
]

# Running the script
iocs = extract_iocs(log_data)
parsed_logs = parse_logs(log_data)
prioritized_alerts = prioritize_alerts(parsed_logs)

# Output results
print("Extracted IOCs:", json.dumps(iocs, indent=2))
print("Parsed Logs with Timestamps:", json.dumps(parsed_logs, indent=2))
print("Prioritized Alerts:", json.dumps(prioritized_alerts, indent=2))

