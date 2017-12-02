from apicalls import *
from predict import *
from flask import Flask, render_template, request
app = Flask(__name__)


def analyze(comp, count = 10):
    company_scores={
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
        company_scores['sadness'] += (s['sadness'] / count)
        company_scores['disgust'] += (s['disgust'] / count)
        company_scores['anger'] += (s['anger'] / count)
        company_scores['joy'] += (s['joy'] / count)
        company_scores['fear'] += (s['fear'] / count)
    return [ company_scores['sadness'],
             company_scores['disgust'],
             company_scores['anger'],
             company_scores['joy'],
             company_scores['fear']]





@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = ['']
    if request.method == "POST":
        company = request.form['company']
        results = analyze(company)
        prediction = predict_change(results)
    return render_template('index.html', prediction=prediction)

if __name__ == "__main__":
    app.run()
