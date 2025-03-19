from pymongo import MongoClient

try:
    client = MongoClient("mongodb://nolet7:securePassword@localhost:27017/?authSource=admin")
    db = client["ids_logs"]
    print("✅ Successfully connected to MongoDB!")

    # Test inserting a document
    db.test_collection.insert_one({"message": "Connection successful!"})
    print("✅ Test document inserted successfully!")

    # Fetch and print the inserted document
    result = db.test_collection.find_one({"message": "Connection successful!"})
    print("Retrieved Document:", result)

except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")

