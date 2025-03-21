from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Replace with your API Key from .env file
API_KEY = os.getenv("API_KEY")
API_URL = "https://jsonwhoisapi.com/api/v1/whois?identifier={}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-domain', methods=['GET'])
def check_domain():
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"error": "Please provide a domain."}), 400

    try:
        headers = {'Authorization': f'Bearer {API_KEY}'}
        response = requests.get(API_URL.format(domain), headers=headers)
        
        # Checking if the response is successful
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch domain info. Status code: {response.status_code}"}), 500
        
        data = response.json()
        
        expiration_date = data.get('expires', 'Not Available')
        owner = data.get('registrant', {}).get('name', 'Private')
        availability = 'Available' if data.get('status') is None else 'Not Available'
        
        return jsonify({
            "domain": domain,
            "availability": availability,
            "expiration_date": expiration_date,
            "owner": owner
        })
    except Exception as e:
        return jsonify({"error": f"Failed to fetch domain info: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
