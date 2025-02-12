import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Load dataset
df = pd.read_csv("cleaned_dataset.csv")

# Rename "text_type" to "label" and map to numerical values
df["label"] = df["text_type"].map({"ham": 0, "spam": 1})  # Convert to 0 and 1

# **Fix Missing Values**
df = df.dropna(subset=["clean_text"])  # Drop rows where "clean_text" is NaN
df["clean_text"] = df["clean_text"].fillna("")  # Replace remaining NaN with empty string

# Feature extraction
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["clean_text"])
y = df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = MultinomialNB()
model.fit(X_train, y_train)

# Save model and vectorizer
joblib.dump(model, "ml_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model training complete! Saved as 'ml_model.pkl' and 'vectorizer.pkl'.")
