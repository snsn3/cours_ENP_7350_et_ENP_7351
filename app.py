#pip install openai==0.28 # install openai library if using this for the first time

from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Initialize the OpenAI API client
openai.api_key = 'Your_KEY'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0125:personal::9eZvvCZe:ckpt-step-65",  
        messages=[{"role": "user", "content": user_input}]
    )
    reply = response.choices[0].message['content']
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
