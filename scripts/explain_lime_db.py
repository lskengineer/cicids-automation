import lime.lime_tabular
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://nolet7:securePassword@localhost:27017/')
db = client['ids_logs']
lime_collection = db['lime_explanations']

# Load the trained model
model = load_model("models/anomaly_detection_model.h5")

# Load dataset (same data used to train the model)
df = pd.read_csv("data/processed_ids_data.csv")

# Ensure 'label' is the correct target column name
X = df.drop('label', axis=1)  # Adjust column name if needed

# Convert model output to 2-class probability format for LIME
def model_predict_proba(X):
    scores = model.predict(X)  
    scores = np.clip(scores, 0, 1)  
    probabilities = np.hstack([1 - scores, scores])  
    return probabilities

# Initialize LIME Explainer
lime_explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X.values,
    feature_names=X.columns,
    mode='classification'
)

# Process multiple instances
lime_data = []
for i in range(min(100, len(X))):  # Limit to first 100 instances
    exp = lime_explainer.explain_instance(X.iloc[i].values, model_predict_proba, num_features=10)
    
    # Store as JSON
    explanation = {
        "index": i,
        "features": list(X.columns),
        "lime_explanation": exp.as_list()
    }
    lime_data.append(explanation)

# Insert into MongoDB
lime_collection.insert_many(lime_data)
print("✅ LIME explanations computed & inserted into MongoDB.")

