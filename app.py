import os
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
from typing_extensions import override
from openai import AssistantEventHandler

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
assistant_id = os.getenv('OPENAI_ASSISTANT_ID') #You can create the assistant in the openai dashboard or through the api.

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

        # Create a Run and stream the response
        class EventHandler(AssistantEventHandler):
            @override
            def on_text_created(self, text) -> None:
                print(f"\nassistant > ", end="", flush=True)

            @override
            def on_text_delta(self, delta, snapshot):
                print(delta.value, end="", flush=True)

            def on_tool_call_created(self, tool_call):
                print(f"\nassistant > {tool_call.type}\n", flush=True)

            def on_tool_call_delta(self, delta, snapshot):
                if delta.type == 'code_interpreter':
                    if delta.code_interpreter.input:
                        print(delta.code_interpreter.input, end="", flush=True)
                    if delta.code_interpreter.outputs:
                        print(f"\n\noutput >", flush=True)
                        for output in delta.code_interpreter.outputs:
                            if output.type == "logs":
                                print(f"\n{output.logs}", flush=True)

        # Stream the run
        with openai.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions="Please address the user appropriately. The user has a standard account.",
            event_handler=EventHandler(),
        ) as stream:
            stream.until_done()

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
