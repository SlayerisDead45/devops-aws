from flask import Flask, request, jsonify
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_cors import CORS  # Added to allow cross-origin requests

load_dotenv()

app = Flask(__name__)
CORS(app) # Keeps communication between apps simple and open

@app.route('/api')
def api_route():
    with open('data.json', 'r') as f:
        my_data = json.load(f)
    return jsonify(my_data)

@app.route('/submit', methods=['POST'])
def handle_form():
    # Read the data sent as JSON from the Node frontend
    data = request.get_json() or {}
    user_text = data.get('content')
    
    if not user_text:
        return jsonify({
            "status": "error", 
            "error_msg": "Error: The box is empty!"
        }), 200

    try:
        uri = os.getenv("MONGO_URI")
        client = MongoClient(uri)
        db = client.my_database
        
        # Save record to cloud collection
        db.my_collection.insert_one({"info": user_text})
        
        return jsonify({"status": "success"})
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "error_msg": f"Database Error: {e}"
        }), 200

if __name__ == '__main__':
    # host='0.0.0.0' is required to make it accessible inside docker
    app.run(host='0.0.0.0', port=5000, debug=True)