from flask import Flask
from flask import url_for, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os, sys, click
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
# initialize database instance
Win = sys.platform.startswith("win")
if Win:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, "data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


# create table classes
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    pwd_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.pwd_hash, password)


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
    user = User(name=name, username=name)
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
@app.errorhandler(405)
def handle_404(e):
    return render_template("404.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.first()
        print(user.name)
        print(user.username)
        print(user.validate_password(password))

        if not username or not password:
            flash("invalid input.")
            return redirect(url_for("login"))
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash("Login success.")
            return redirect(url_for("index"))

        flash("invalid username and password.")
        return redirect(url_for("login"))
    else:
        return render_template('login.html')


@app.route("/logout", )
@login_required
def logout():
    logout_user()
    flash("Goodbye")
    return redirect(url_for("index"))


@app.route("/", methods=['GET', 'POST'])
@app.route("/home")
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("unauthenticated user!")
            return redirect(url_for("index"))
        title = request.form.get('name')
        year = request.form.get('year')
        if not title or not year or len(year) >4 or len(title) >60:
            flash('invalid input')
            return redirect(url_for('index'))
        novel = Novel(title=title, year=year)
        db.session.add(novel)
        db.session.commit()
        flash("item added!")
        return redirect(url_for('index'))
    novels = Novel.query.all()
    rendered_text = render_template("index.html", novels=novels)
    return rendered_text


@app.route("/settings", methods=["POST", "GET"])
@login_required
def settings():
    if request.method == "POST":
        name = request.form["name"]
        if not name or len(name)>20:
            flash("invalid input.")
            return redirect(url_for("settings"))
        current_user.name = name
        db.session.commit()
        flash("Settings updated.")
        return redirect(url_for("index"))

    return render_template('settings.html')


@app.route('/edit_novel/id_<int:novel_id>', methods=['GET', 'POST'])
@login_required
def edit(novel_id):
    novel = Novel.query.get_or_404(novel_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(title) > 60 or len(year) > 4:
            flash("Invalid input.")
            return redirect(url_for('edit', novel_id=novel_id))
        novel.title = title
        novel.year = year
        db.session.commit()
        flash("Item updated")
        return redirect(url_for("index"))
    return render_template('edit.html', novel=novel)


@app.route('/delete_novel/id_<int:novel_id>', methods=['POST'])
@login_required
def delete(novel_id):
    print(novel_id)
    novel = Novel.query.get_or_404(novel_id)
    db.session.delete(novel)
    db.session.commit()
    flash("Item deleted")
    return redirect(url_for("index"))


@app.cli.command()
@click.option("--username", prompt=True, help="the usename used to login.")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="the password used to login")
def admin(username, password):
    """create user"""
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo("Updating user ...")
        user.username = username
        user.set_password(password)
    else:
        click.echo("Creating user ...")
        user = User(username=username, name="Admin")
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo("Done.")

