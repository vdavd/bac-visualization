from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, session, flash, abort
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
    del session["id"]
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
    
    if len(password1) < 7:
        flash("Username or password too short")
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

@app.route("/new_room", methods=["POST"])
def new_room():
    room_name = request.form["new_room"]

    sql = text("SELECT id FROM rooms WHERE room_name=:new_room")
    result = db.session.execute(sql, {"new_room":room_name})

    if result.fetchone():
        flash("Room name is already taken")
        return redirect("/rooms")
    else:
        try:
            sql = text("INSERT INTO rooms (owner_id, room_name) VALUES (:owner_id, :new_room) RETURNING id")
            result = db.session.execute(sql, {"owner_id":session["id"], "new_room":room_name})
            room_id = result.fetchone()[0]
            sql = text("INSERT INTO members (room_id, member_id) VALUES (:room_id, :member_id)")
            db.session.execute(sql, {"room_id":room_id, "member_id":session["id"]})
            db.session.commit()
            flash("Room creation was succesful")
            return redirect("/rooms")
        except:
            flash("Room name too short")
            return redirect("/rooms")
        
@app.route("/join_room", methods=["POST"])
def join_room():
    room_name = request.form["join_room"]

    sql = text("SELECT id FROM rooms WHERE room_name=:join_room")
    result = db.session.execute(sql, {"join_room":room_name})
    result = result.fetchone()
    print(result)
    if result:
        try:
            room_id = result[0]
            sql = text("INSERT INTO members (room_id, member_id) VALUES (:room_id, :member_id)")
            db.session.execute(sql, {"room_id":room_id, "member_id":session["id"]})
            db.session.commit()
            flash("You succesfully joined the room")
            return redirect("/rooms")
        except:
            flash("You are already a member of this room")
            return redirect("/rooms")
    else:
        flash("Room does not exist")
        return redirect("/rooms")
    
@app.route("/rooms")
def rooms():
    sql = text("SELECT m.room_id, r.room_name FROM members m INNER JOIN rooms r ON r.id = m.room_id WHERE m.member_id=:user_id")
    result = db.session.execute(sql, {"user_id":session["id"]})
    my_rooms = result.fetchall()
    return render_template("rooms.html", my_rooms=my_rooms)

@app.route("/room/<int:room_id>")
def room(room_id):
    sql = text("SELECT id FROM members WHERE room_id=:room_id AND member_id=:user_id")
    result = db.session.execute(sql, {"room_id":room_id, "user_id":session["id"]})
    if not result.fetchone():
        abort(403)

    sql = text("SELECT u.username, r.room_name FROM rooms r INNER JOIN members m ON r.id = m.room_id INNER JOIN users u ON m.member_id = u.id WHERE m.room_id=:room_id")
    result = db.session.execute(sql, {"room_id":room_id})
    room_members = result.fetchall()
    return render_template("room.html", room_members = room_members)
