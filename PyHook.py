#!/usr/bin/env python3
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def HandleWebhook():
    data = request.json
    print(data)
    return "OK", 200

app.run(host = "", port=9001)
