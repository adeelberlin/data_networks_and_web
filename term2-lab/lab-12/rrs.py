from flask import Flask
import feedparser
from random import randint

app = Flask(__name__)

CNN_FEED = "http://rss.cnn.com/rss/edition.rss"

@app.route("/")
def headline():
    feed = feedparser.parse(CNN_FEED)
    article = feed['entries'][1]

    return """<html>
    <body>
    <h1> CNN HEADLINE </h1>
    <b>{0}</b> <br/>
    <i>{1}</i> <br/>
    <p>{2}</p> <br/>
    </body>
    </html>""".format(article.get("title"),
    article.get("published"), article.get("summary"))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)

