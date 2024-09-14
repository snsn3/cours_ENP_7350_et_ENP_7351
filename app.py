from flask import Flask, render_template, request, jsonify
import os
import time
from openai import OpenAI

app = Flask(__name__)

# Initialize the OpenAI API client
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

ASSISTANT_ID = os.getenv('ASSISTANT_ID')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    try:
        # Create a thread with the user's message
        thread = client.beta.threads.create(
            messages=[{"role": "user", "content": user_input}]
        )

        # Submit the thread to the assistant (as a new run)
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

        # Wait for the run to complete
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            time.sleep(1)

        # Get the latest message from the thread
        message_response = client.beta.threads.messages.list(thread_id=thread.id)
        messages = message_response.data

        # Extract the assistant's reply
        latest_message = messages[0].content[0].text.value

        return jsonify({'reply': latest_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
