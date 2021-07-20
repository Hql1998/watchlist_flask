from flask import Flask
import flask

print(__name__)

app = Flask(__name__)

@app.route("/")
def hello():
    return """
    <h2> Hello World! My beautiful friend!</h2>
    <button type="submit" formaction="newdoc">Click Me!</button>
    """

@app.route("/newdoc")
def new_doc():
    return '<img src="https://ss2.baidu.com/-vo3dSag_xI4khGko9WTAnF6hhy/baike/pic/item/cf1b9d16fdfaaf513e010cc4875494eef11f7aef.jpg">'