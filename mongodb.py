from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["test"]  # Replace with the actual name
collection = db["messages"]

# Fetch all messages
messages = collection.find()

for msg in messages:
    print(msg)
