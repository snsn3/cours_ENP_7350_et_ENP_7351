from flask import Flask, render_template, request, jsonify
import openai
import os
######## ....#######
app = Flask(__name__)
# initialize=ing the OpenAI client through - when possible use env variables to ensure privacy
openai.api_key = os.getenv('OPENAI_API_KEY')
assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
# the app - this is UI designed in templates folder
@app.route('/')
def index():
    return render_template('index.html')
# routing the chat app
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    thread = client.beta.threads.create()
        thread_id=thread.id,
        role="user",
        content=user_input
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    messages = client.beta.threads.messages.create(thread_id=thread.id)
    assistant_reply = next((msg['content'] for msg in messages['messages'] if msg['role'] == 'assistant'), "I'm being trained as a policy assistant!")
    return jsonify({'reply': assistant_reply})
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
