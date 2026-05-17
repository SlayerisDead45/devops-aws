from flask import Flask, render_template, request, redirect, jsonify
import json
import os  # Read from system environment variables
from dotenv import load_dotenv  # Load the .env file cleanly
from pymongo import MongoClient

# Initialize loading environment variables from your .env file
load_dotenv()

app = Flask(__name__)

# 1. THE API ROUTE
@app.route('/api')
def api_route():
    # Read the local data storage file
    with open('data.json', 'r') as f:
        my_data = json.load(f)
    return jsonify(my_data)

# 2. THE FORM PAGE
@app.route('/')
def home():
    return render_template('index.html')

# 3. HANDLING THE FORM SUBMISSION
@app.route('/submit', methods=['POST'])
def handle_form():
    user_text = request.form.get('content')
    
    # Simple validation fallback
    if not user_text:
        return render_template('index.html', error_msg="Error: The box is empty!")
        
    try:
        # Dynamically read your sensitive string from .env
        uri = os.getenv("MONGO_URI")
        
        client = MongoClient(uri)
        db = client.my_database
        db.my_collection.insert_one({"info": user_text})
        
        # If it works, go to the success page
        return redirect('/success')
    except Exception as e:
        # If it fails, show the error on the same page
        return render_template('index.html', error_msg=f"Database Error: {e}")

@app.route('/success')
def success():
    return "Data submitted successfully"

if __name__ == '__main__':
    app.run(debug=True)