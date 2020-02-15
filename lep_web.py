import flask

import lep_parser


app = flask.Flask(__name__)


@app.route("/")
def index():
    articles = sorted(lep_parser.get_front_page_articles(), key=lambda a: a.section)
    return flask.render_template("index.html", articles=articles)
