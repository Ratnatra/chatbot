# app.py
from flask import Flask, request, jsonify, render_template_string
from chatbot import get_response

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<title>Customer Support Chatbot</title>
<h2>Customer Support Chatbot</h2>
<div id="chatbox" style="width: 400px; height: 300px; border: 1px solid #888; padding: 10px; overflow-y: auto; margin-bottom: 10px;"></div>
<input id="userInput" type="text" style="width: 300px;">
<button onclick="sendMessage()">Send</button>

<script>
let chatbox = document.getElementById('chatbox');
function sendMessage() {
    let userInput = document.getElementById('userInput');
    let message = userInput.value;
    if (!message) return;
    chatbox.innerHTML += '<b>You:</b> ' + message + '<br>';
    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: message})
    }).then(res => res.json()).then(data => {
        chatbox.innerHTML += '<b>Bot:</b> ' + data.response + '<br>';
        chatbox.scrollTop = chatbox.scrollHeight;
    });
    userInput.value = '';
}
document.getElementById('userInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') sendMessage();
});
</script>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    bot_response = get_response(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)