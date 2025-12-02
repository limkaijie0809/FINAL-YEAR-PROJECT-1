from flask import Flask, jsonify
from flask_cors import CORS  # allow frontend to call backend

app = Flask(__name__)
CORS(app)  # enable CORS so JS from browser can access the API

@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})

# 👉 This is your first API endpoint
@app.route("/api/start-training", methods=["GET"])
def start_training():
    sample_question = {
        "id": 1,
        "email_subject": "Your account has been suspended!",
        "email_body": "Dear user, your account will be terminated. Click here to verify your identity.",
        "is_phishing": True
    }
    return jsonify(sample_question)

if __name__ == "__main__":
    app.run(debug=True)
