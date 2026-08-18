# 🤖 Hugging Face Sentiment Analysis with Flask & MongoDB Atlas

A simple AI-powered web application that performs sentiment analysis using a pre-trained Hugging Face model, Flask, and MongoDB Atlas.

## 🚀 Features

- Hugging Face pre-trained NLP model
- Sentiment analysis
- Positive / Negative prediction
- Confidence score
- Flask web interface
- MongoDB Atlas cloud database
- Stores AI prediction results

## 🛠️ Technologies

- Python
- Flask
- Hugging Face Transformers
- DistilBERT
- PyTorch
- MongoDB Atlas
- PyMongo
- HTML/CSS

## 🧠 Hugging Face Model

**Model:** `distilbert/distilbert-base-uncased-finetuned-sst-2-english`

**Hugging Face:**  
https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english

The model predicts:

- POSITIVE
- NEGATIVE

## 📁 Project Structure

huggingface-sentiment/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
├── .gitignore
│
└── templates/
    └── index.html
## ⚙️ Installation

Clone the Repository
git clone https://github.com/YOUR-USERNAME/huggingface-sentiment.git
cd huggingface-sentiment
Create Virtual Environment
python -m venv .venv

Windows:

.venv\Scripts\activate
## Install Dependencies
pip install -r requirements.txt
🗄️ MongoDB Atlas

## Create a MongoDB Atlas database:

Database: AI_Sentiment_DB
Collection: sentiment_results

Create a .env file:

MONGO_URI=your_mongodb_atlas_connection_string

Do not upload .env to GitHub.

## ▶️ Run the Application
python app.py

Open:

http://127.0.0.1:5000
## 🔄 Workflow
User Input
    ↓
Flask Web Application
    ↓
Hugging Face Model
    ↓
Sentiment + Confidence
    ↓
MongoDB Atlas
    ↓
## Store AI Result
🧪 Example
Input
The product is excellent and I really enjoyed using it.
Output
Sentiment: POSITIVE
Confidence: 0.99

The result is stored in MongoDB Atlas.

📌 MongoDB Document
{
  "text": "The product is excellent",
  "sentiment": "POSITIVE",
  "confidence": 0.99,
  "model": "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
}
🔐 Security

Add the following to .gitignore:

.env
.venv/
__pycache__/
*.pyc

Never commit:

MongoDB passwords
MongoDB connection strings
API keys
Secret credentials
🎯 Learning Outcomes
AI-as-a-Service
NLP and Sentiment Analysis
Hugging Face Model Integration
Flask Application Development
MongoDB Atlas Integration
AI-powered Cloud Application
