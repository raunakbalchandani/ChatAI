from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import openai
import traceback

app = Flask(__name__)
CORS(app)

# Set up your OpenAI API key
openai.api_key = 'open-ai-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_packages.db'
db = SQLAlchemy(app)

class TravelPackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    price = db.Column(db.Float)
    details = db.Column(db.String(200))

# Create database tables
with app.app_context():
    db.create_all()

def query_chatgpt(question):
    response = openai.Completion.create(
        engine="davinci",
        prompt=question,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def query_travel_packages(origin, destination):
    packages = TravelPackage.query.filter_by(origin=origin, destination=destination).all()
    if not packages:
        return "No travel packages found."
    return [f"Package to {p.destination} from {p.origin}: ${p.price}. Details: {p.details}" for p in packages]

@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        app.logger.info(f"Received data: {data}")
        if not data or 'question' not in data:
            return jsonify({"answer": "Invalid request format."}), 400
        
        question = data.get('question')
        
        if "distance" in question or "flight time" in question:
            answer = query_chatgpt(question)
        else:
            if "Mumbai" in question:
                origin = "Mumbai"
            elif "Hong Kong" in question:
                origin = "Hong Kong"
            else:
                return jsonify({"answer": "Origin city not recognized."}), 400

            if "London" in question:
                destination = "London"
            else:
                return jsonify({"answer": "Destination city not recognized."}), 400

            packages = query_travel_packages(origin, destination)
            answer = '\n'.join(packages)
        
        return jsonify({"answer": answer})
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"answer": "An error occurred processing your request."}), 500

if __name__ == '__main__':
    app.run(debug=True)
