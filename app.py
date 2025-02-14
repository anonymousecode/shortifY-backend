from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Hugging Face API key
HUGGINGFACE_API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {
    "Authorization": f"Bearer {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}"
}

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "No text provided."}), 400

    payload = {"inputs": text, "parameters": {"max_length": 500, "min_length": 50, "do_sample": False}}

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return jsonify({"summary": response.json()[0]["summary_text"]})
    else:
        return jsonify({"error": response.json().get('error', 'Unknown error')}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
