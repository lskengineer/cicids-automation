from pymongo import MongoClient

MONGO_URI = "mongodb://nolet7:securePassword@192.168.0.119:27017/admin"
client = MongoClient(MONGO_URI)

try:
    db = client["ids_logs"]
    collection = db["shap_explanations"]
    sample = collection.find_one()
    print("Connected to MongoDB! Sample Data:", sample)
except Exception as e:
    print("MongoDB Connection Error:", e)

