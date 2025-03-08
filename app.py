import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
# Initialize OpenAI client with API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
assistant_id = os.getenv('OPENAI_ASSISTANT_ID')

# UI route
@app.route('/')
def index():
    return render_template('index.html')

# Chat route
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Create a new thread
        thread = openai.beta.threads.create()

        # Add user's message to the thread
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        # Create a run to process the thread with the assistant
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Poll the run status until it's completed
        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == 'completed':
                break
            elif run_status.status in ['failed', 'cancelled', 'expired']:
                return jsonify({'error': f'Run failed with status: {run_status.status}'}), 500
            import time
            time.sleep(1) #avoid overwhelming the API

        # Retrieve the messages from the thread
        messages = openai.beta.threads.messages.list(thread_id=thread.id)

        # Get the assistant's reply (last message from the assistant)
        assistant_reply = next(
            (msg.content[0].text.value for msg in reversed(messages.data) if msg.role == 'assistant' and msg.content),
            "I'm being trained as a policy assistant!"
        )

        return jsonify({'reply': assistant_reply})

    except Exception as e:
        print(f"Error processing chat: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
