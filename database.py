from pymongo import MongoClient
from utility import load_config

# Load configuration
config = load_config()
mongo_config = config.get("mongodb", {})
client = MongoClient(mongo_config.get("host", "localhost"), mongo_config.get("port", 27017))
db = client[mongo_config.get("database", "crybit_db")]

def store_scam_message(data):
    """Store a flagged scam message in the database."""
    db.scam_messages.insert_one(data)

def get_scam_messages(query={}):
    """Retrieve flagged scam messages from the database."""
    return list(db.scam_messages.find(query))

def clear_scam_messages():
    """Delete all flagged scam messages from the database."""
    db.scam_messages.delete_many({})

def add_monitored_channel(channel_id):
    """Add a new channel to the monitored channels list."""
    if not db.monitored_channels.find_one({"channel_id": channel_id}):
        db.monitored_channels.insert_one({"channel_id": channel_id})

def get_monitored_channels():
    """Retrieve all monitored Telegram channels."""
    return list(db.monitored_channels.find())

def remove_monitored_channel(channel_id):
    """Remove a channel from the monitored channels list."""
    db.monitored_channels.delete_one({"channel_id": channel_id})

def clear_monitored_channels():
    """Clear all monitored Telegram channels from the database."""
    db.monitored_channels.delete_many({})
