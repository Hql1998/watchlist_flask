from flask import Flask
from flask import url_for, render_template

print(__name__)

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def hello():
    rendered_text = render_template("index.html", name=name, novels=novels)
    return rendered_text

@app.route("/user/<name>")
def new_doc(name):
    print(url_for('hello'))
    return '<p>user is {0}</p><img src="https://ss2.baidu.com/-vo3dSag_xI4khGko9WTAnF6hhy/baike/pic/item/cf1b9d16fdfaaf513e010cc4875494eef11f7aef.jpg">'.format(name)

@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('new_doc', name='greyli', year=12))  # 输出：/user/greyli
    print(url_for('new_doc', name='peter', year=14))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'

name = 'H Ql'
novels = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]