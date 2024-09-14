from flask import Flask, render_template, request, jsonify
import os
import time
import openai

app = Flask(__name__)

# Initialize the OpenAI API client
openai.api_key = os.getenv('OPENAI_API_KEY')

ASSISTANT_ID = os.getenv('ASSISTANT_ID')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    try:
        # Create a thread with the user's message
        thread = openai.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        # Submit the thread to the assistant (as a new run)
        run = openai.beta.threads.runs.create(
            thread_id=thread['id'], 
            assistant_id=ASSISTANT_ID
        )

        # Wait for the run to complete by polling its status
        while run['status'] != "completed":
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread['id'], 
                run_id=run['id']
            )
            time.sleep(1)

        # Retrieve the message from the completed thread
        message_response = openai.beta.threads.messages.retrieve(
            thread_id=thread['id'], 
            message_id=run['id']
        )

        message_content = message_response['content'][0]['text']['value']
        
        # You can include annotations if needed
        # annotations = message_response['content'][0]['text']['annotations']

        return jsonify({'reply': message_content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
