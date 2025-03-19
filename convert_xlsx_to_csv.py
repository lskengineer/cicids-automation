import pandas as pd

# Define input and output file paths
input_file = "/home/nolet7/cicids-automation/data/ids_data_combined.xlsx"
output_file = "/home/nolet7/cicids-automation/data/ids_data_combined.csv"

# Load the Excel file
df = pd.read_excel(input_file, sheet_name=None)  # Load all sheets

# If multiple sheets exist, merge them into a single CSV
if isinstance(df, dict):
    combined_df = pd.concat(df.values(), ignore_index=True)
else:
    combined_df = df

# Save to CSV
combined_df.to_csv(output_file, index=False)

print(f"✅ Conversion Completed! CSV saved at: {output_file}")

