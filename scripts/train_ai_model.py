from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import pandas as pd

# Load CSV
df = pd.read_csv("data/processed_ids_data.csv")

# Ensure column names are properly formatted
df.columns = df.columns.str.strip()  # Remove leading/trailing spaces

# Drop unnecessary columns that cannot be used in training
df = df.drop(['flow_id', 'timestamp', 'src_ip', 'dst_ip', 'ftp_patator'], axis=1, errors='ignore')

# Convert categorical features ('protocol') using Label Encoding
if 'protocol' in df.columns:
    df['protocol'] = LabelEncoder().fit_transform(df['protocol'])

# Ensure 'label' column is correctly formatted
df['label'] = LabelEncoder().fit_transform(df['label'])

# Convert all data to float32 (TensorFlow requirement)
df = df.astype('float32')

# Separate features and target variable
X = df.drop('label', axis=1)
y = df['label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Build neural network model
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),  # Define input layer correctly
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')  # For binary classification
])

# Compile model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Save trained model
model.save('models/anomaly_detection_model.keras')  # Save in Keras native format

print("✅ AI Model Training Completed!")

