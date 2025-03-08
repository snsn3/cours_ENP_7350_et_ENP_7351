from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# initialize client 
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
#app
@app.route('/')
def index():
    return render_template('index.html')
#app  route
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = client.chat.completions.create(
        model="gpt-4o-mini",  #model choice as of oct. 2024
        messages=[{"role": "user", "content": user_input}]
    )
    reply = response.choices[0].message['content']
    return jsonify({'reply': reply})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
