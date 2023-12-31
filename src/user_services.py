import secrets
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return True
        return False

def logout():
    del session["username"]
    del session["id"]
    del session["csrf_token"]

def check_availability(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    if result.fetchone():
        return False
    return True

def check_spaces(username):
    if " " in username:
        return False
    return True

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def get_profile():
    sql = text("SELECT user_weight, user_height, user_age, sex FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":session["id"]})
    return result.fetchone()

def check_profile():
    user_info = get_profile()
    for info in user_info:
        if not info:
            return False
    return True

def edit_profile(sex, weight, height, age):
    sql = text("UPDATE users SET sex=:sex, user_weight=:weight, \
               user_height=:height, user_age=:age WHERE id=:user_id")
    db.session.execute(sql, {"sex":sex, "weight":weight, "height":height, \
                             "age":age, "user_id":session["id"]})
    db.session.commit()

def check_token(csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)
