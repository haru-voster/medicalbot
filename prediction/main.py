from flask import Flask, request, jsonify
from flask_cors import CORS
from chat import get_response  

app = Flask(__name__)
CORS(app)  

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Chatbot API is running! Use POST to chat."})

@app.route("/chat", methods=["POST"])  # 🚀 Only POST Allowed
def chat():
    try:
        data = request.get_json()
        if "message" not in data:
            return jsonify({"error": "Missing 'message' field"}), 400

        user_message = data["message"]
        bot_response = get_response(user_message)  # Call chatbot function
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"🔥 ERROR: {e}")  # Print error in terminal
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
