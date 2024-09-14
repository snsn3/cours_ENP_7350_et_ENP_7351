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
        run = openai.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

        # Wait for the run to complete
        while run.status != "completed":
            run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            time.sleep(1)

        # Retrieve the message from the completed thread
        message_response = openai.beta.threads.messages.retrieve(thread_id=thread.id, message_id=run.id)
        message_content = message_response.content[0].text.value
        annotations = message_response.content[0].text.annotations

        # Process any annotations or citations
        citations = []
        for index, annotation in enumerate(annotations):
            # Replace the text with a footnote
            message_content = message_content.replace(annotation.text, f' [{index}]')

            # Handle file citations if present
            if (file_citation := getattr(annotation, 'file_citation', None)):
                cited_file = openai.files.retrieve(file_citation.file_id)
                citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
            elif (file_path := getattr(annotation, 'file_path', None)):
                cited_file = openai.files.retrieve(file_path.file_id)
                citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
        
        # Append citations to the message
        message_content += '\n' + '\n'.join(citations)

        return jsonify({'reply': message_content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
