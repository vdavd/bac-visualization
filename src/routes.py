from app import app
from flask import redirect, render_template, request, session, flash, abort
from sqlalchemy.sql import text
from db import db
import user_services
import drink_services
import room_services
import plot_services

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    
    username = request.form["username"]
    password = request.form["password"]

    if user_services.login(username, password):
        return redirect("/")
    else:
        flash("Incorrect username or password")
        return redirect("/")

@app.route("/logout")
def logout():
    user_services.logout()
    return redirect("/")

@app.route("/new_account")
def new_account():
    return render_template("new_account.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not user_services.check_username(username):
        flash("Username is already taken")
        return redirect("/new_account")
    
    if len(password1) < 7 or len(username) < 3:
        flash("Username has to be 3 characters or longer \
              and password has to be 8 characters or longer")
        return redirect("/new_account")
    
    if password1 == password2:
        if not user_services.register(username, password1):
            flash("Username has to be 3 characters or longer \
                  and password has to be 8 characters or longer")
            return redirect("/new_account")
        else:
            return redirect("/account_created")
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
    drink = request.form["drink"]
    drink_time = request.form["drink_time"]
    if not drink_time:
        flash("Please choose a date and time")
        return redirect("new_drink")
    drink_services.add_drink(drink, drink_time)
    return redirect("/")

@app.route("/list_drinks")
def list_drinks():
    user_drinks = drink_services.get_user_drinks()
    user_drinks = user_drinks[::-1]
    return render_template("list_drinks.html", user_drinks=user_drinks)

@app.route("/new_room", methods=["POST"])
def new_room():
    room_name = request.form["new_room"]
    if room_services.check_room_name(room_name):
        flash("Room name is already taken")
        return redirect("/rooms")
    else:
        if room_services.new_room(room_name):
            flash("Room creation was succesful")
            return redirect("/rooms")
        else:
            flash("Room name is too short")
            return redirect("/rooms")
        
@app.route("/join_room", methods=["POST"])
def join_room():
    room_name = request.form["room_to_join"]
    room_id = room_services.check_room_name(room_name)
    if room_id:
        if room_services.join_room(room_id):
            flash("You succesfully joined the room")
            return redirect("/rooms")
        else:
            flash("You are already a member of this room")
            return redirect("/rooms")
    else:
        flash("Room does not exist")
        return redirect("/rooms")
    
@app.route("/rooms")
def rooms():
    my_rooms = room_services.list_rooms()
    return render_template("rooms.html", my_rooms=my_rooms)

@app.route("/room/<int:room_id>")
def room(room_id):
    permission = room_services.check_permission(room_id)
    if not permission:
        abort(403)

    room_members = room_services.list_members(room_id)
    return render_template("room.html", room_members = room_members)

@app.route("/bac_plot")
def bac_plot():
    user_drinks = drink_services.get_user_drinks()
    bac_df, time_now = plot_services.calculate_bac(user_drinks)
    plot_services.plot_bac(bac_df, time_now)
    return render_template("bac_plot.html")

@app.route("/profile")
def profile():
    user_info = user_services.get_profile()
    return render_template("profile.html", user_info = user_info)

@app.route("/edit_profile", methods=["POST"])
def edit_profile():
    sex = request.form["sex"]
    try:
        weight = int(request.form["weight"])
        height = int(request.form["height"])
        age = int(request.form["age"])
    except:
        flash("Weight and height must be numbers")
        return redirect("/profile")
    user_services.edit_profile(sex, weight, height, age)
    flash("Profile was updated")
    return redirect("/profile")