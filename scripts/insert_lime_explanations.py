import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ids_logs"]
lime_collection = db["lime_explanations"]

# Load LIME results
df = pd.read_csv("data/lime_results.csv")

# Convert DataFrame to list of dictionaries
lime_records = df.to_dict(orient="records")

# Insert into MongoDB
lime_collection.insert_many(lime_records)

print(f"✅ Inserted {len(lime_records)} LIME explanations into MongoDB")

