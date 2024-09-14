from flask import Flask, render_template, request, jsonify
import os
import time
import openai 

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

ASSISTANT_ID = os.getenv('ASSISTANT_ID')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    # Create a completion with OpenAI's GPT-4 model
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        
        # Extract the assistant's reply
        reply = response['choices'][0]['message']['content']
        
        return jsonify({'reply': reply})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
