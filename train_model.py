import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("data/books.csv")

# Replace missing values
df.fillna("", inplace=True)

# Combine important features
df["tags"] = (
    df["genre"] + " " +
    df["description"] + " " +
    df["author"]
)

# Create TF-IDF vectors
tfidf = TfidfVectorizer(stop_words="english")
vectors = tfidf.fit_transform(df["tags"])

# Calculate similarity
similarity = cosine_similarity(vectors)

# Save model
joblib.dump(df, "model/books.pkl")
joblib.dump(similarity, "model/similarity.pkl")

print("✅ Recommendation model trained successfully!")