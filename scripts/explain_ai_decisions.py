import shap
import lime.lime_tabular
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from pymongo import MongoClient

# Load AI Model
model = load_model("models/anomaly_detection_model.h5")

# Load Dataset
df = pd.read_csv("data/processed_ids_data.csv")
X = df.drop('label', axis=1)  # Ensure lowercase 'label'

# Initialize MongoDB Connection
client = MongoClient("mongodb://nolet7:securePassword@localhost:27017/?authSource=admin")
db = client["ids_logs"]
xia_collection = db["xia_explanations"]

# Ensure Model Returns Probabilities for LIME
def predict_proba(X):
    preds = model.predict(X)
    if preds.shape[1] == 1:  # If binary classification
        return np.hstack((1 - preds, preds))  # Convert single probability to two-class format
    return preds  # Multi-class models already output probabilities

# --------------------------- SHAP Explanation ----------------------------

try:
    explainer = shap.KernelExplainer(model.predict, X.iloc[:100])  # Use a subset for explainer
    shap_values = explainer.shap_values(X.iloc[0:10])  # Get SHAP values for first 10 rows

    shap_data = []
    for i in range(len(shap_values)):
        shap_data.append({
            "index": i,
            "features": list(X.columns),
            "shap_values": shap_values[i].tolist()
        })

    print("✅ SHAP explanations computed successfully!")

except Exception as e:
    print(f"❌ Error computing SHAP values: {e}")
    shap_data = []

# --------------------------- LIME Explanation ----------------------------

try:
    lime_explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=X.values,
        feature_names=X.columns,
        mode='classification'
    )

    lime_explanations = []
    for i in range(10):
        exp = lime_explainer.explain_instance(X.iloc[i].values, predict_proba, num_features=5)
        lime_explanations.append({"index": i, "lime_explanation": exp.as_list()})

    print("✅ LIME explanations computed successfully!")

except Exception as e:
    print(f"❌ Error computing LIME explanations: {e}")
    lime_explanations = []

# --------------------------- Store in MongoDB ----------------------------

if shap_data or lime_explanations:
    xia_collection.insert_many(shap_data + lime_explanations)
    print("✅ XIA Data Stored in MongoDB")
else:
    print("⚠️ No data inserted into MongoDB due to errors.")

