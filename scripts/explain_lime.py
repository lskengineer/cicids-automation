import lime.lime_tabular
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model("models/anomaly_detection_model.h5")

# Load dataset (ensure correct path)
df = pd.read_csv("data/processed_ids_data.csv")
X = df.drop(columns=["label"], errors="ignore")  # Drop 'label' if it exists

# --------------------------- LIME Explanation ----------------------------

# Function to convert model output to binary class probabilities
def model_predict_proba(X):
    """Convert model anomaly scores to binary class probabilities for LIME"""
    scores = model.predict(X)  # Get raw anomaly scores
    scores = np.clip(scores, 0, 1)  # Ensure scores are between 0 and 1
    probabilities = np.hstack([1 - scores, scores])  # Convert to 2-class probability
    return probabilities

# Initialize LIME explainer
lime_explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X.values,
    feature_names=X.columns,
    mode='classification'
)

# Generate LIME explanations
lime_results = []
for i in range(100):  # Process first 100 rows
    exp = lime_explainer.explain_instance(X.iloc[i].values, model_predict_proba, num_features=10)
    lime_results.append({
        "index": i,
        "features": exp.as_list()
    })

# Convert to DataFrame
lime_df = pd.DataFrame(lime_results)

# Save to CSV for database insertion
lime_df.to_csv("data/lime_results.csv", index=False)
print("✅ LIME explanations saved to data/lime_results.csv")

