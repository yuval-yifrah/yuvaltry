import random
from flask import Flask, request

app = Flask(__name__)

phrase = ["צוקי אני אוהבת אותך","בוקי טוי צוקיהו","מתי תאילנד"]

@app.route("/")
def index():
    random_phrase = random.choice(phrase)
    return f'{random_phrase}!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
