from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

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
            return True
        else:
            return False
        
def logout():
    del session["username"]
    del session["id"]

def check_username(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})

    if result.fetchone():
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
    sql = text("SELECT user_weight, sex FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":session["id"]})
    return result.fetchone()

def edit_profile(sex, weight):
    sql = text("UPDATE users SET sex=:sex, user_weight=:weight WHERE id=:user_id")
    db.session.execute(sql, {"sex":sex, "weight":weight, "user_id":session["id"]})
    db.session.commit()