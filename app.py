from flask import Flask, render_template, request
from transformers import pipeline
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
import os
from datetime import datetime

app = Flask(__name__)

# Load .env
load_dotenv(override=True)

# -----------------------------
# MongoDB Atlas
# -----------------------------

MONGO_URI = os.getenv("MONGODB_URI")

if not MONGO_URI:
    raise ValueError("MONGODB_URI is not found in .env")

# Check what URI is being loaded
print("MongoDB URI starts with:", MONGO_URI[:20])

if not MONGO_URI.startswith("mongodb+srv://"):
    raise ValueError(
        "MONGODB_URI is not a MongoDB Atlas connection string. "
        "It should start with mongodb+srv://"
    )

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

# ACTUALLY test the connection
try:
    client.admin.command("ping")
    print("MongoDB Atlas connected successfully!")
except Exception as e:
    print("MongoDB Atlas connection failed!")
    print(e)
    raise

db = client["AI_Sentiment_DB"]
collection = db["sentiment_results"]


# -----------------------------
# Hugging Face
# -----------------------------

MODEL_NAME = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

print("Loading Hugging Face model...")

sentiment_model = pipeline(
    "sentiment-analysis",
    model=MODEL_NAME
)

print("Hugging Face model loaded successfully!")


# -----------------------------
# Flask Route
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    text = None
    sentiment = None
    confidence = None

    if request.method == "POST":

        text = request.form["text"]

        if text.strip():

            # Hugging Face prediction
            result = sentiment_model(text)[0]

            sentiment = result["label"]
            confidence = round(result["score"], 4)

            # MongoDB document
            document = {
                "text": text,
                "sentiment": sentiment,
                "confidence": confidence,
                "model": MODEL_NAME,
                "created_at": datetime.now()
            }

            # Save to MongoDB Atlas
            collection.insert_one(document)

            print("Sentiment result saved to MongoDB Atlas!")

    return render_template(
        "index.html",
        text=text,
        sentiment=sentiment,
        confidence=confidence
    )


if __name__ == "__main__":
    app.run(debug=True)