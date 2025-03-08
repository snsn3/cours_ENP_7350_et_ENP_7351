from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Initialize OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message')

        if not user_input:
            return jsonify({'error': 'Missing message in request'}), 400

        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Use a valid model name
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message['content']
        return jsonify({'reply': reply})

    except openai.error.OpenAIError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000)) #gets the port number from the enviroment variables, or defaults to 5000.
    app.run(host='0.0.0.0', port=port)
