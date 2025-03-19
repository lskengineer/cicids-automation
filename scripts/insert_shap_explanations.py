import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ids_logs"]
shap_collection = db["shap_explanations"]

# Load SHAP results
df = pd.read_csv("data/shap_results.csv")

# Convert DataFrame to list of dictionaries
shap_records = df.to_dict(orient="records")

# Insert into MongoDB
shap_collection.insert_many(shap_records)

print(f"✅ Inserted {len(shap_records)} SHAP explanations into MongoDB")

