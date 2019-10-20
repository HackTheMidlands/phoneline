from flask import Flask, request

from .app import voice, sms

app = Flask(__name__)

@app.route('/voice', methods=['POST', 'GET'])
def test_voice():
    return voice(request)

@app.route('/sms', methods=['POST', 'GET'])
def test_sms():
    return sms(request)
