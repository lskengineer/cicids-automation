import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE

# Load CSV Data
csv_file = "data/ids_data_combined.csv"
df = pd.read_csv(csv_file)

# Drop unnecessary columns
drop_cols = ["flow_id", "timestamp", "src_ip", "dst_ip", "protocol"]
df.drop(columns=drop_cols, inplace=True, errors='ignore')

# Convert categorical 'label' column to binary (0 = Benign, 1 = Attack)
df['label'] = np.where(df['label'] == 'Benign', 0, 1)

# Normalize numerical features
scaler = StandardScaler()
numeric_cols = df.drop(columns=['label']).columns  # All except 'label'
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# Handle Class Imbalance using SMOTE (if dataset is imbalanced)
benign_count = df['label'].value_counts()[0]
attack_count = df['label'].value_counts()[1]

if benign_count > 2 * attack_count:  # If 'Benign' is too dominant
    print("Applying SMOTE to balance dataset...")
    smote = SMOTE(sampling_strategy=0.5)  # Ensure at least 50% attack traffic
    X_resampled, y_resampled = smote.fit_resample(df.drop(columns=['label']), df['label'])
    df = pd.DataFrame(X_resampled, columns=numeric_cols)
    df['label'] = y_resampled

# Save preprocessed data
df.to_csv("data/processed_ids_data.csv", index=False)
print("✅ Data Preprocessing Completed!")

