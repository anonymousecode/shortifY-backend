from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

# Fetch API Key from environment variables
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    raise ValueError("API Key not found! Make sure to set it in Render.")

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided."}), 400

        payload = {"inputs": text, "parameters": {"max_length": 500, "min_length": 50, "do_sample": False}}

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            summary_text = response.json()[0].get("summary_text", "No summary generated.")
            return jsonify({"summary": summary_text})
        else:
            return jsonify({"error": response.json().get('error', 'Unknown error')}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
