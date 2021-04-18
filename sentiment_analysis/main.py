from flask import Blueprint, Flask, session, render_template, jsonify, request
from sentiment_analysis.Analyze import score as score_text
from sentiment_analysis.Analyze import topTags
from base64 import b64decode as b64d
import requests as r
import json
from sentiment_analysis.Utils.sentiment import Sentiment
import logging


sentiment = Blueprint("sentiment", __name__, 
    template_folder="templates", 
    static_folder="static", 
    static_url_path="/sentiment_analysis/static" 
)

port=8000


with open('sentiment_analysis/config.json') as f:
    config = json.load(f)
    
@sentiment.route('/')
def index():
    if session.get('text') is None:
        session['text'] = ""
        session['last_response']=""
    return render_template('index.html')

@sentiment.route('/score', methods=["GET","POST"])
def score():
    if request.method == "POST":

        content = request.json['content']
        avg, good, bad = score_text(content)

        return jsonify({
            'score': avg,
            'good': good,
            'bad': bad,
            'top_tags': topTags(good, bad, 3)
        })
    return False

@sentiment.route('/finalScore', methods=["GET","POST"])
def finalScore():
    if request.method == "POST":
        text = request.json['content']
        if(text == session.get('text')):
           return jsonify(Sentiment(session.get('last_response')).getData())
        subscription_key = config['subscription_key']
        endpoint = config['endpoint']
        sentiment_url = endpoint + "/text/analytics/v3.1-preview.1/sentiment?opinionMining=true" #now on 3.1
        documents = {"documents": [
        {"id": "1", "language": "en",
        "text": text},]}
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        response = r.post(sentiment_url, headers=headers, json=documents)
        sentiments = response.json()
        session['text'] = text
        session['last_response'] = sentiments
        res = jsonify(Sentiment(sentiments).getData())
        return res        
    return ""
