from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Initialize the OpenAI API client
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
	@@ -14,12 +16,33 @@ def index():
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  
        messages=[{"role": "user", "content": user_input}]
    )
    reply = response.choices[0].message['content']
    return jsonify({'reply': reply})
