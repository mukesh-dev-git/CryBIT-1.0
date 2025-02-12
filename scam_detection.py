import re
import joblib
import requests
import torch
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
import easyocr
from utility import load_config, save_to_mongodb

# Load config
config = load_config()
ml_model_path = config["ml_model"]["model_path"]
scam_keywords = config["scam_detection"]["scam_keywords"]

# Load ML Model
try:
    model = joblib.load(ml_model_path)
except FileNotFoundError:
    model = None
    print("Warning: ML model not found. Train a model and save it as ml_model.pkl.")

# Load trained TF-IDF vectorizer
try:
    vectorizer = joblib.load("vectorizer.pkl")  # Load trained TF-IDF vectorizer
except FileNotFoundError:
    vectorizer = None
    print("Warning: TF-IDF vectorizer not found. Train and save it as vectorizer.pkl.")

# Load Transformer Model for NLP
transformer_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load OCR Model
easyocr_reader = easyocr.Reader(['en'])

def analyze_message(message_text):
    """Analyze a message for scam detection."""
    risk_score = 0
    flags = []
    
    # Keyword-based detection
    if any(keyword in message_text.lower() for keyword in scam_keywords):
        risk_score += 0.5
        flags.append("Keyword Match")
    
    # ML Model Prediction
    if model and vectorizer:
        message_vector = vectorizer.transform([message_text])  # Use pre-trained vectorizer
        prediction = model.predict_proba(message_vector)[0][1]
        risk_score += prediction
        if prediction > 0.3:
            flags.append("ML Model Prediction")
    
    # Sentence Transformer Embeddings for Semantic Analysis
    embedding = transformer_model.encode(message_text, convert_to_tensor=True)
    if torch.mean(embedding).item() > 0.1:
        risk_score += 0.2
        flags.append("Semantic Analysis")
    
    return {"message": message_text, "risk_score": risk_score, "flags": flags, "is_scam": risk_score > config["scam_detection"]["risk_threshold"]}

def inspect_url(url):
    """Check if a URL is phishing using Google Safe Browsing API."""
    api_key = config["api_keys"]["google_safe_browsing"]
    response = requests.post(
        f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}",
        json={"client": {"clientId": "crybit", "clientVersion": "1.0"},
              "threatInfo": {"threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                             "platformTypes": ["ANY_PLATFORM"],
                             "threatEntryTypes": ["URL"],
                             "threatEntries": [{"url": url}]}}
    )
    result = response.json()
    return {"url": url, "is_phishing": "matches" in result}

def check_wallet_address(wallet):
    """Check if a crypto wallet address is blacklisted."""
    api_key = config["api_keys"]["scam_wallet"]
    response = requests.get(f"https://api.scamwalletchecker.com/check/{wallet}?apiKey={api_key}")
    result = response.json()
    return {"wallet": wallet, "is_blacklisted": result.get("blacklisted", False)}

def extract_text_from_image(image_path):
    """Extract text from an image using OCR."""
    return " ".join(easyocr_reader.readtext(image_path, detail=0))

def save_scam_message(message_data):
    """Save a detected scam message to MongoDB."""
    save_to_mongodb(message_data, "scam_messages")