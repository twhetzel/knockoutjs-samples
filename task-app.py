from flask import Flask, request, redirect, render_template, session, jsonify
import urllib
import urlparse
import json, requests
import pandas as pd
from xml.etree import ElementTree as ET
import io

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("task-list.html")

@app.route("/tasks")
def tasks():
    allData = [{"title": "wash cat", "isDone": False}, {"title": "do something", "isDone": True}]
    return jsonify(allData)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)