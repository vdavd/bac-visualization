from flask import session
from sqlalchemy.sql import text
from db import db

def add_drink(drink, drink_time):
    sql = text("SELECT id FROM choices WHERE drink_name=:drink")
    result = db.session.execute(sql, {"drink":drink})
    drink_id = result.fetchone()[0]
    sql = text("INSERT INTO drinks (user_id, drink_id, drink_time) \
               VALUES (:user_id, :drink_id, :drink_time)")
    db.session.execute(sql, {"user_id":session["id"], "drink_id":drink_id, "drink_time":drink_time})
    db.session.commit()

def get_user_drinks(user_id):
    sql = text("SELECT u.username, u.sex, u.user_weight, u.user_height, \
               u.user_age, c.alcohol_content, d.drink_id, c.drink_name, \
               d.drink_time FROM users u LEFT JOIN drinks d ON u.id=d.user_id LEFT JOIN \
               choices c ON c.id=d.drink_id WHERE u.id=:user_id ORDER BY d.drink_time")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_drinks_summary(user_id):
    sql = text("SELECT COUNT(d.drink_id), c.category FROM drinks d LEFT JOIN choices c \
               ON d.drink_id=c.id WHERE d.user_id=:user_id GROUP BY c.category")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()
