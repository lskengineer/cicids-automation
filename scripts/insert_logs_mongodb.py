from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient('mongodb://nolet7:securePassword@localhost:27017/')
db = client['ids_logs']
logs_collection = db['logs']
shap_collection = db['shap_explanations']
lime_collection = db['lime_explanations']

# Path to alert log file
log_file = '/var/log/snort/alert.fast'  

try:
    with open(log_file, 'r') as file:
        for i, line in enumerate(file):
            # Fetch corresponding SHAP & LIME explanations
            shap_exp = shap_collection.find_one({"index": i})
            lime_exp = lime_collection.find_one({"index": i})
            
            log_entry = {
                "index": i,
                "alert": line.strip(),
                "shap_explanation": shap_exp["shap_values"] if shap_exp else None,
                "lime_explanation": lime_exp["lime_explanation"] if lime_exp else None
            }

            logs_collection.insert_one(log_entry)

    print("✅ Logs, SHAP, and LIME explanations inserted into MongoDB.")

except Exception as e:
    print(f"❌ Error while inserting logs: {e}")

