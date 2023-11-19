from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    
    username = request.form["username"]
    password = request.form["password"]

    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        flash("Incorrect username or password")
        return redirect("/")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["id"] = user.id
            return redirect("/")
        else:
            flash("Incorrect username or password")
            return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new_account")
def new_account():
    return render_template("new_account.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})

    if result.fetchone():
        flash("Username is already taken")
        return (redirect("/new_account"))
    
    if password1 == password2:
        hash_value = generate_password_hash(password1)
        try:
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
            return redirect("/account_created")
        except:
            flash("Username or password too short")
            return (redirect("/new_account"))
    else:
        flash("Passwords do not match")
        return redirect("/new_account")
    
@app.route("/account_created")
def account_created():
    return render_template("account_created.html")

@app.route("/new_drink")
def new_drink():
    return render_template("new_drink.html")

@app.route("/add_drink", methods=["POST"])
def add_drink():
    juoma = request.form["juoma"]
    sql = text("SELECT id FROM choices WHERE drink_name=:juoma")
    result = db.session.execute(sql, {"juoma":juoma})
    print(result)
    drink_id = result.fetchone()[0]
    sql = text("INSERT INTO drinks (user_id, drink_id, drink_time) VALUES (:user_id, :drink_id, NOW())")
    db.session.execute(sql, {"user_id":session["id"], "drink_id":drink_id})
    db.session.commit()
    return redirect("/")

@app.route("/list_drinks")
def list_drinks():
    sql = text("SELECT c.drink_name, d.drink_time FROM drinks d INNER JOIN choices c ON c.id = d.drink_id WHERE d.user_id=:user_id ORDER BY d.id DESC")
    result = db.session.execute(sql, {"user_id":session["id"]})
    juomat = result.fetchall()
    return render_template("list_drinks.html", juomat=juomat)