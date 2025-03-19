import shap
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model("models/anomaly_detection_model.h5")

# Load dataset (ensure correct path)
df = pd.read_csv("data/processed_ids_data.csv")
X = df.drop(columns=["label"], errors="ignore")  # Drop 'label' if it exists

# --------------------------- SHAP Explanation ----------------------------

# Create SHAP explainer
explainer = shap.KernelExplainer(model.predict, X.iloc[:100])  # Use a subset

# Compute SHAP values
shap_values = explainer.shap_values(X.iloc[:100])

# Convert SHAP values to NumPy array & squeeze to remove extra dimension
shap_values = np.array(shap_values).squeeze()  # Fix shape issue

# Print SHAP value shape after squeezing
print(f"SHAP values shape after squeezing: {shap_values.shape}")

# Convert to DataFrame
shap_df = pd.DataFrame(shap_values, columns=X.columns)

# Save to CSV for database insertion
shap_df.to_csv("data/shap_results.csv", index=False)
print("✅ SHAP explanations saved to data/shap_results.csv")

