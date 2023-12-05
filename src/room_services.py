from db import db
from flask import session
from sqlalchemy.sql import text

# check_room_name checks if room with a given name exists
# returns room_id if the room exists, return False if not
def check_room_name(room_name):
    sql = text("SELECT id FROM rooms WHERE room_name=:room_name")
    result = db.session.execute(sql, {"room_name":room_name})
    room_id = result.fetchone()
    if room_id:
       return room_id[0]
    return False

def new_room(room_name):
    try:
        sql = text("INSERT INTO rooms (owner_id, room_name) VALUES (:owner_id, :new_room) RETURNING id")
        result = db.session.execute(sql, {"owner_id":session["id"], "new_room":room_name})
        room_id = result.fetchone()[0]
        sql = text("INSERT INTO members (room_id, member_id) VALUES (:room_id, :member_id)")
        db.session.execute(sql, {"room_id":room_id, "member_id":session["id"]})
        db.session.commit()
        return True
    except:
        return False
    
def join_room(room_id):
    try:
        sql = text("INSERT INTO members (room_id, member_id) VALUES (:room_id, :member_id)")
        db.session.execute(sql, {"room_id":room_id, "member_id":session["id"]})
        db.session.commit()
        return True
    except:
        return False
    
def list_rooms():
    sql = text("SELECT m.room_id, r.room_name FROM members m INNER JOIN rooms r \
               ON r.id = m.room_id WHERE m.member_id=:user_id")
    result = db.session.execute(sql, {"user_id":session["id"]})
    return result.fetchall()

def check_permission(room_id):
    sql = text("SELECT id FROM members WHERE room_id=:room_id AND member_id=:user_id")
    result = db.session.execute(sql, {"room_id":room_id, "user_id":session["id"]})
    if result.fetchone():
        return True
    else:
        return False
    
def list_members(room_id):
    sql = text("SELECT u.id, u.username, r.room_name FROM rooms r INNER JOIN members m \
               ON r.id = m.room_id INNER JOIN users u ON m.member_id = u.id WHERE m.room_id=:room_id")
    result = db.session.execute(sql, {"room_id":room_id})
    return result.fetchall()