from utility import fetch_from_mongodb
scam_messages = fetch_from_mongodb("scam_messages")
print(scam_messages)  # ✅ This should return a list of stored scam messages
