# chatbot.py
import random

RESPONSES = {
    "hello": ["Hello! How can I help you today?", "Hi there! What can I do for you?"],
    "order": ["Can you provide your order number?", "I'd be happy to help with your order. What's the order number?"],
    "refund": ["I'm sorry to hear you want a refund. Can you provide your order number?"],
    "problem": ["I'm sorry you're experiencing a problem. Can you describe it in more detail?"],
    "bye": ["Goodbye! Have a great day.", "Bye! If you have more questions, feel free to ask."],
}

DEFAULT_RESPONSE = "Sorry, I didn't understand that. Can you please rephrase your question?"

def get_response(message):
    msg = message.lower()
    for keyword, replies in RESPONSES.items():
        if keyword in msg:
            return random.choice(replies)
    return DEFAULT_RESPONSE