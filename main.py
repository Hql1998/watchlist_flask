from flask import Flask
from flask import url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import os, sys, click


app = Flask(__name__)


# initialize database instance
Win = sys.platform.startswith("win")
if Win:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, "data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



# create table classes
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),)
class Novel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


# initialize databases
@app.cli.command()
@click.option("--drop", is_flag=True, help="create after drop.")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')
    create_table_data()
    click.echo('records created.')
    query_table()
    update_table()
    click.echo('table updated.')
    delet_records()


def create_table_data():
    from main import User, Novel
    user = User(name="hql")
    novel1 = Novel(title="Leon", year="1994")
    novel2 = Novel(title="mahjon", year="1996")
    db.session.add(user)
    db.session.add(novel1)
    db.session.add(novel2)
    db.session.commit()

def query_table():
    from main import Novel
    novel = Novel.query.first()
    print(novel.id, novel.title, novel.year)
    print(Novel.query.count())
    print(Novel.query.filter_by(title="mahjon").all())
    print(Novel.query.filter(Novel.year == "1994").first())

def update_table():
    from main import Novel, User
    user2 = User(name="zz")
    novel3 = Novel(title="beautiful day", year="2013")
    for i in [user2, novel3]:
        db.session.add(i)
    novel2 = Novel.query.filter_by(year="1996").first()
    print("update_table novel2", novel2)
    novel2.year = "2020"
    print("update_table novel2", novel2.year)
    db.session.commit()

def delet_records():
    from main import User
    print("delet_records")
    users = User.query.all()
    for i in users:
        print(i.name)
    db.session.delete(i)
    db.session.commit()
    print(User.query.count())


@app.cli.command()
def forge():
    db.drop_all()
    db.create_all()

    name = "hql"
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
    user = User(name=name)
    db.session.add(user)

    for n in novels:
        novel = Novel(title=n['title'], year=n['year'])
        db.session.add(novel)

    db.session.commit()
    click.echo("database forged")


@app.context_processor
def inject_global():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def handle_404(e):
    return render_template("404.html")

@app.route("/")
@app.route("/home")
def index():
    novels = Novel.query.all()
    rendered_text = render_template("index.html", novels=novels)
    return rendered_text

@app.route("/user/<name>")
def new_doc(name):
    print(url_for('hello'))
    return '<p>user is {0}</p>' \
           '<img src="{1}">'.format(name, "./static/image/brown.jpg")

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
