import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from googletrans import Translator
import os

lemmatizer = WordNetLemmatizer()

# Get the absolute path to the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use the correct absolute path for intents.json, words.pkl, classes.pkl, and chatbot_model.h5
intents = json.loads(open(os.path.join(BASE_DIR, '../intents.json'), encoding='utf-8').read())
words = pickle.load(open(os.path.join(BASE_DIR, '../words.pkl'), 'rb'))
classes = pickle.load(open(os.path.join(BASE_DIR, '../classes.pkl'), 'rb'))
model = load_model(os.path.join(BASE_DIR, '../chatbot_model.h5'))
translator = Translator()

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence, words)
    res = model.predict(np.array([bow]))[0]
    
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            response = random.choice(i['responses'])
            break
        
    return response
def get_bot_response(message, lang='en'):
    # Detect language if not specified
    if lang == 'auto':
        detected = translator.detect(message)
        lang = detected.lang
    else:
        detected = None
    # Translate to English if not English
    if lang != 'en':
        translated_input = translator.translate(message, dest='en').text
    else:
        translated_input = message
    intents_list = predict_class(translated_input)
    response = get_response(intents_list, intents)
    # Translate response back to user's language if needed
    if lang != 'en':
        response = translator.translate(response, dest=lang).text
    return response

if __name__ == "__main__":
    print("Chatbot is ready to talk! Type 'quit' to exit.")
    while True:
        message = input("")
        if message.lower() == 'quit':
            break
        response = get_bot_response(message, lang='auto')
        print(response)