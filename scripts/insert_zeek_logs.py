from pymongo import MongoClient
import os
import csv

# Connect to MongoDB
client = MongoClient('mongodb://nolet7:securePassword@localhost:27017/?authSource=admin')
db = client['ids_logs']
alerts_collection = db['alerts']

# Path to Zeek log files
log_directory = '/opt/zeek/logs/current/'

try:
    # Loop through Zeek logs in the directory
    for log_file in os.listdir(log_directory):
        if log_file.endswith('.log'):  # Check if it's a Zeek log file (e.g., conn.log)
            log_file_path = os.path.join(log_directory, log_file)

            with open(log_file_path, 'r') as file:
                # Read the log file as CSV (space-separated or tab-separated)
                reader = csv.reader(file, delimiter=' ')  # Split by space
                
                for row in reader:
                    # Remove empty spaces from the row
                    row = [field.strip() for field in row if field.strip()]

                    # Skip empty rows or malformed rows with fewer columns than expected
                    if not row or len(row) < 6:  # Modify the length condition based on expected columns
                        continue
                    
                    print(f"Processing row: {row}")  # Print the row for debugging
                    
                    try:
                        alert = {
                            "timestamp": row[0],
                            "client_id": row[1],
                            "src_ip": row[2],
                            "src_port": row[3],
                            "dst_ip": row[4],
                            "dst_port": row[5],
                            "protocol": row[6] if len(row) > 6 else None,
                            "log_data": row[7:]  # Capture any remaining fields
                        }
                        # Insert the alert into MongoDB
                        alerts_collection.insert_one(alert)
                    except IndexError as e:
                        print(f"Error processing row: {row} | Error: {e}")
                        continue  # Skip malformed rows

    print("✅ Zeek log insertion completed!")
except Exception as e:
    print(f"Error while reading Zeek log files: {e}")

