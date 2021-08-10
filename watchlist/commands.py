import click
from watchlist import db, app
from watchlist.models import User, Novel


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