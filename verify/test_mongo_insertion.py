from pymongo import MongoClient

def test_mongo_connection():
    try:
        # Updated connection string with authentication
        client = MongoClient("mongodb://admin:admin@localhost:27017/")
        db = client["identity_verification_db"]
        collection = db["identityinfo"]

        # Insert a test document
        test_doc = {"test_field": "test_value"}
        insert_result = collection.insert_one(test_doc)
        print(f"Inserted document ID: {insert_result.inserted_id}")

        # Retrieve the document
        retrieved_doc = collection.find_one({"_id": insert_result.inserted_id})
        print(f"Retrieved document: {retrieved_doc}")

        # Clean up: delete the test document
        collection.delete_one({"_id": insert_result.inserted_id})
        print("Test document deleted successfully.")

        print("MongoDB connection and insertion test succeeded.")
    except Exception as e:
        print(f"MongoDB connection or insertion test failed: {e}")

if __name__ == "__main__":
    test_mongo_connection()
