from apicalls import *
from predict import *
from flask import Flask, render_template, request
app = Flask(__name__)


def analyze(comp, count = 10):
    company_scores[comp]={
        'sadness': 0,
        'disgust': 0,
        'anger': 0,
        'joy': 0,
        'fear': 0
    }
    score=[]
    response = twitget(comp, count)
    tweets = response['statuses']
    for tweet in tweets:
        result = watsget(comp,tweet['full_text'])
        score.append(result['emotion']['document']['emotion'])
    for s in score:
        company_scores[comp]['sadness'] += (s['sadness'] / count)
        company_scores[comp]['disgust'] += (s['disgust'] / count)
        company_scores[comp]['anger'] += (s['anger'] / count)
        company_scores[comp]['joy'] += (s['joy'] / count)
        company_scores[comp]['fear'] += (s['fear'] / count)
    return [ company_scores[comp]['sadness'],
             company_scores[comp]['disgust'],
             company_scores[comp]['anger'],
             company_scores[comp]['joy'],
             company_scores[comp]['fear']]





@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = ['hi']
    if request.method == "POST":
        company = request.form['company']
        prediction = ['worked']
        # results = analyze(company)
        # prediction = predict_change(results)
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
