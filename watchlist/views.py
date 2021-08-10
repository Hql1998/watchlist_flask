from flask import url_for, render_template, request, redirect, flash
from watchlist import db, app
from watchlist.models import User, Novel
from flask_login import login_user, login_required, current_user,logout_user

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


@app.errorhandler(404)
@app.errorhandler(405)
def handle_404(e):
    return render_template("404.html")