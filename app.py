#pip install openai==0.28 # install openai library if using this for the first time

from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Initialize the OpenAI API client
openai.api_key = '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'

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
