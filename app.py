from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

# Headers for the OpenAI API call
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# Serve main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the chat functionality
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.get_json().get('message')

    # Define the payload to be sent to the OpenAI API
    payload = {
        "messages": [{"role": "user", "content": user_input}]
    }

    try:
        # Make the POST request to the specific assistant endpoint
        response = requests.post(
            f"https://api.openai.com/v1/assistants/{ASSISTANT_ID}/completions",
            headers=HEADERS,
            json=payload
        )

        # Check if the request was successful
        if response.status_code == 200:
            assistant_reply = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            return jsonify({'reply': assistant_reply})
        else:
            # Handle errors (e.g., authentication issues, bad requests)
            return jsonify({'error': response.json().get('error', 'Unknown error')}), response.status_code

    except Exception as e:
        # Handle exceptions (e.g., network issues)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
