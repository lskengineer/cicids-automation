import shap
import lime.lime_tabular
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import numpy as np

# Load the trained model
model = load_model("models/anomaly_detection_model.h5")

# Load the dataset (same data that was used to train the model)
df = pd.read_csv("data/processed_ids_data.csv")

# Ensure 'label' is the correct target column name
X = df.drop('label', axis=1)  # Change 'label' if needed

# --------------------------- SHAP Explanation ----------------------------

# Create a SHAP explainer object
explainer = shap.KernelExplainer(model.predict, X.iloc[:100])  # Use a subset for explainer

# Compute SHAP values
shap_values = explainer.shap_values(X.iloc[:100])  # Get SHAP values for first 100 rows

# Print SHAP value shape
print(f"SHAP values shape before squeezing: {np.array(shap_values).shape}")

# Remove extra dimension if present
shap_values_fixed = np.squeeze(np.array(shap_values))  # Squeeze to remove extra dimension

# Print the updated SHAP value shape
print(f"SHAP values shape after squeezing: {shap_values_fixed.shape}")

# Save SHAP Summary Plot
shap.summary_plot(shap_values_fixed, X.iloc[:100], show=False)  # Prevent interactive plotting
plt.savefig("shap_summary_plot.png")
plt.close()

# --------------------------- SHAP Force Plot (Fixed) ----------------------------

# Check dimensions before plotting
if shap_values_fixed.shape[1] != X.shape[1]:  
    print(f" ERROR: SHAP values length {shap_values_fixed.shape[1]} != Feature length {X.shape[1]}")
else:
    print("✅ SHAP values and feature vector match!")

# Create Explanation object for Matplotlib
explainer_obj = shap.Explanation(
    values=shap_values_fixed[0],  # Take the first row's SHAP values
    base_values=explainer.expected_value[0], 
    data=X.iloc[0].values, 
    feature_names=X.columns
)

# Fix: Use Matplotlib for force plot
shap.initjs()  # Prevents interactive JS errors
plt.figure(figsize=(10, 4))  # Set figure size
shap.force_plot(explainer.expected_value[0], shap_values_fixed[0], X.iloc[0], matplotlib=True)
plt.savefig("shap_force_plot.png")  # Save force plot
plt.close()  # Free memory

print("✅ SHAP force plot saved successfully!")

# --------------------------- LIME Explanation ----------------------------

# LIME Explanation
lime_explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=X.values,
    feature_names=X.columns,
    mode='classification'
)

# Explain the first instance
exp = lime_explainer.explain_instance(X.iloc[0].values, model.predict, num_features=10)

# Save the LIME explanation plot
exp.as_pyplot_figure()
plt.savefig("lime_explanation.png")
plt.close()

print("✅ LIME visualization completed!")

