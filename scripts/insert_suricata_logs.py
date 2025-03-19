from pymongo import MongoClient
import json

# Connect to MongoDB with your existing user credentials
client = MongoClient('mongodb://nolet7:securePassword@localhost:27017/?authSource=admin')
db = client['ids_logs']
alerts_collection = db['alerts']

# Path to Suricata log file
log_file = '/var/log/suricata/eve.json'

try:
    with open(log_file, 'r') as file:
        for line in file:
            try:
                # Skip empty lines and parse valid JSON lines
                if line.strip():  # Ignore empty lines
                    alert = json.loads(line.strip())  # Parse JSON line into a Python dictionary
                    alerts_collection.insert_one(alert)
            except json.JSONDecodeError:
                # Log an error message and skip invalid JSON lines
                print(f"Skipping invalid JSON line: {line.strip()}")
    print("✅ Suricata log insertion completed!")
except Exception as e:
    print(f"Error while reading Suricata log file: {e}")

