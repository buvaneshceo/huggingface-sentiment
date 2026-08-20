from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import requests
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
    raise ValueError("MONGODB_URI is not found in environment variables")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

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
# Hugging Face Inference API
# -----------------------------

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is not found in environment variables")

MODEL_NAME = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

HF_API_URL = (
    f"https://router.huggingface.co/hf-inference/models/{MODEL_NAME}"
)

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

print("Hugging Face Inference API configured successfully!")


# -----------------------------
# Flask Route
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    text = None
    sentiment = None
    confidence = None
    error = None

    if request.method == "POST":

        text = request.form.get("text", "").strip()

        if not text:

            error = "Please enter some text."

        else:

            try:

                # Send text to Hugging Face
                response = requests.post(
                    HF_API_URL,
                    headers=headers,
                    json={
                        "inputs": text
                    },
                    timeout=60
                )

                result = response.json()

                print("Hugging Face Response:")
                print(result)

                # Check API response
                if response.status_code != 200:

                    error = str(result)

                else:

                    # Hugging Face returns:
                    # [[{'label': 'POSITIVE', 'score': 0.99}]]

                    prediction = result[0]

                    sentiment = prediction["label"]

                    confidence = round(
                        prediction["score"],
                        4
                    )

                    # -----------------------------
                    # Save Result to MongoDB Atlas
                    # -----------------------------

                    document = {
                        "text": text,
                        "sentiment": sentiment,
                        "confidence": confidence,
                        "model": MODEL_NAME,
                        "created_at": datetime.now()
                    }

                    collection.insert_one(document)

                    print(
                        "Sentiment result saved to MongoDB Atlas!"
                    )

            except Exception as e:

                print("Error:", e)

                error = str(e)

    return render_template(
        "index.html",
        text=text,
        sentiment=sentiment,
        confidence=confidence,
        error=error
    )


# -----------------------------
# Run Application
# -----------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
