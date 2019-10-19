from flask import Flask, request

from .app import voice

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def test():
    return voice(request)