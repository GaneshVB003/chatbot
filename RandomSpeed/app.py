from flask import Flask, request, jsonify , send_file
from flask_cors import CORS
import google.generativeai as genai
import os 


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Set up Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route('/')
def home():
    return send_file('index.html')


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"reply": "Please enter a message."})

        # Generate response from Gemini API
        response = model.generate_content(user_message)

        return jsonify({"reply": response.text})
    
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
