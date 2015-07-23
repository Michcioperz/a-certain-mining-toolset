#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, request
import json

app = Flask(__name__)
stuff = []

@app.route("/data/orly")
def data():
	stuff.append(json.loads(request.args['orly']))
	return "richtig"

@app.route("/save/stuff")
def save():
	with open("orly.json", "w") as file:
		file.write(json.dumps(stuff, indent=2, sort_keys=True))
	return "richtig"

if __name__ == "__main__":
	app.run(debug=True)
