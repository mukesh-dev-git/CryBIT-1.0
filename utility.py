import json
import os
from pymongo import MongoClient

def load_config(config_path="config.json"):
    """Load configuration from a JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError("Config file not found!")
    with open(config_path, "r") as file:
        return json.load(file)

def get_mongo_client():
    """Initialize and return a MongoDB client."""
    config = load_config()
    mongo_config = config.get("mongodb", {})
    client = MongoClient(mongo_config.get("host", "localhost"), mongo_config.get("port", 27017))
    return client[mongo_config.get("database", "crybit_db")]

def save_to_mongodb(data, collection_name):
    """Save data to MongoDB collection."""
    db = get_mongo_client()
    collection = db[collection_name]
    collection.insert_one(data)

def fetch_from_mongodb(collection_name, query={}):
    """Fetch data from MongoDB collection based on query."""
    db = get_mongo_client()
    collection = db[collection_name]
    return list(collection.find(query))

def delete_from_mongodb(collection_name, query={}):
    """Delete records from MongoDB based on query."""
    db = get_mongo_client()
    collection = db[collection_name]
    collection.delete_many(query)
