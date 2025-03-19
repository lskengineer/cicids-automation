import shap
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://nolet7:securePassword@localhost:27017/')
db = client['ids_logs']
shap_collection = db['shap_explanations']

# Load the trained model
model = load_model("models/anomaly_detection_model.h5")

# Load dataset
df = pd.read_csv("data/processed_ids_data.csv")

# Ensure 'label' is the correct target column name
X = df.drop('label', axis=1)

# SHAP Explainer
explainer = shap.KernelExplainer(model.predict, X.iloc[:100])  # Limit for efficiency
shap_values = explainer.shap_values(X.iloc[:100])  # Compute SHAP for first 100 rows

# Store SHAP results in MongoDB
shap_data = []
for i in range(len(X.iloc[:100])):
    explanation = {
        "index": i,
        "features": list(X.columns),
        "shap_values": shap_values[i].tolist()
    }
    shap_data.append(explanation)

# Insert into MongoDB
shap_collection.insert_many(shap_data)
print("✅ SHAP explanations computed & inserted into MongoDB.")

