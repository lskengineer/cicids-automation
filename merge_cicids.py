import pandas as pd
import os
import shutil

# Function to load the datasets
def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Loaded {os.path.basename(file_path)} with {len(df)} rows")
        return df
    except Exception as e:
        print(f"⚠️ Error processing {os.path.basename(file_path)}: {e}")
        return None

# List of all files to be processed
files = [
    "ftp_patator.csv", "ddos_loit.csv", "dos_hulk_sample.csv", "dos_hulk_fixed.csv", 
    "dos_hulk_with_measurement.csv", "portscan.csv", "friday_benign.csv", "dos_golden_eye.csv",
    "web_brute_force.csv", "wednesday_benign.csv", "monday_benign.csv", "thursday_benign.csv", 
    "dos_slowloris.csv", "dos_slowhttptest.csv", "merged_ids_data.csv", "dos_hulk.csv", 
    "dos_hulk_clean.csv", "ssh_patator-new.csv", "heartbleed.csv", "tuesday_benign.csv", 
    "dos_hulk_clean_fixed.csv", "botnet_ares.csv", "dos_hulk_trimmed.csv", "web_sql_injection.csv", 
    "web_xss.csv"
]

# Initialize an empty DataFrame for merging
merged_data = pd.DataFrame()

# Directory where the files are located
directory = "/home/nolet7/cicids2017/BCCC-CIC-IDS-2017/"

# Merge files without removing problematic columns
for file_name in files:
    file_path = os.path.join(directory, file_name)
    df = load_csv(file_path)
    
    if df is not None:
        merged_data = pd.concat([merged_data, df], ignore_index=True)

# Save the merged dataset
merged_file_path = "/home/nolet7/cicids2017/BCCC-CIC-IDS-2017/merged_ids_data.csv"
merged_data.to_csv(merged_file_path, index=False)
print(f"✅ Merging Completed! Dataset saved at: {merged_file_path}")

# Now, copy the merged data to your specified location on your laptop
destination_path = '/mnt/c/Users/Lateef/Downloads/merged_ids_data.csv'

# Copy the merged CSV file to the desired location
shutil.copy(merged_file_path, destination_path)
print(f"✅ Dataset successfully copied to: {destination_path}")

