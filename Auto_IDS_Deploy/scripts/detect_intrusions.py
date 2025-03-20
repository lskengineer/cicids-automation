import pymongo
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("../models/ids_model.h5")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ids_logs"]
alerts = db["alerts"]

def classify_traffic(features):
    prediction = model.predict(np.array([features]))[0]
    return "Malicious" if prediction > 0.5 else "Benign"

def log_alert(features):
    alert_data = {"features": features, "prediction": classify_traffic(features)}
    alerts.insert_one(alert_data)
    print(f"Alert Logged: {alert_data}")

log_alert([0.2, 0.5, 0.1, 0.9])
