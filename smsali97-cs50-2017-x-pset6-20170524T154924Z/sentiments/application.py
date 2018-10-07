from flask import Flask, redirect, render_template, request, url_for

import os
import sys
import helpers
import nltk
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    tokenizer = nltk.tokenize.TweetTokenizer()

    # validate screen_name
    screen_name = request.args.get("screen_name", "").lstrip("@")
    if not screen_name:
        return redirect(url_for("index"))
        
    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")    
        
    analyzer = Analyzer(positives, negatives)    

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    if tweets == None :
        return redirect(url_for("index"))
    
    ctr = 0
    hap = 0
    sad = 0
    neu = 0

    for tweet in tweets:
        val = 0
        score = 0
        tokens = tokenizer.tokenize(tweet)
        for token in tokens:
            val += analyzer.analyze(token)
        score = val
        ctr += 1
        if  score > 0 :
            hap += 1
        elif score < 0 :
            sad += 1
        else: 
            neu += 1
    
    positive, negative, neutral = hap/ctr * 100, sad/ctr * 100, neu/ctr * 100

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
