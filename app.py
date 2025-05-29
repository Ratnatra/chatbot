from flask import Flask, request, jsonify
import chatbot
import os

app = Flask(__name__, static_folder='.', template_folder='.')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    # Detect language automatically and reply in that language
    response = chatbot.get_bot_response(user_message, lang='auto')
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)