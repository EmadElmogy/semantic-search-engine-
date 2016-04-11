# -*- coding: utf-8 -*-
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask, render_template, request, url_for
#from urllib import quote_plus
import freebase
import goslate
import wikipedia



# Initialize the Flask application
app = Flask(__name__)

gs = goslate.Goslate()
# Define a route for the default URL, which loads the index
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for the action of the index, for example '/engine/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/engine/', methods=['POST'])
def engine():
    # Get question from user as text
    question =request.form['question']
    #unicode_question=unicode(question, "utf-8")
    # Send question to api for question analysis and generate query
    # this Online App is An example For apply Quepy Model on DBpedia
    # We use it only as a quick demo but we have alot we need to do ..
    url = "http://quepy.machinalis.com/engine/get_query?question="+question
    #gs.translate(text, 'de', 'en')
    # encoded_url = quote_plus(url.encode("utf-8"))
    #   Get sparql query as json
    r = requests.get(url)
    j = r.json()
    # Select only the sparql code
    query = (j['queries'][0]['query'])
    # Send sparql-query to SPARQLWrapper Model to run it on dbpedia
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    # Get results as json
    results = sparql.query().convert()
    #convert question string to array
    q2=question.split(' ')
    wiki_question = wikipedia.summary(question)
    # return json to answer page to view.
    return render_template('answer.html', question=question, results=results , q2=q2 , wiki_question=wiki_question)

# Run the app :)
if __name__ == '__main__':
  app.run(debug=True)

