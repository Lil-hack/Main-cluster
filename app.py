import json
import threading
import os
from flask import Flask, jsonify, g
import sqlite3

try:
    from ssh_client import send
except:
    print('no paramilo')
app = Flask(__name__)

file_name='minecraft.db'
path = os.path.dirname(os.path.abspath(__file__))+'/'

LIFE=10
KILL=5
WIN=50



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(path+"minecraft.db")

    return db

@app.teardown_appcontext
def close_cursorection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("CREATE TABLE users (name TEXT , password TEXT, money INTEGER, life INTEGER, wins INTEGER ,kills INTEGER, dies INTEGER)")
    cursor.execute("INSERT INTO users VALUES ('1234', 'eee', 0,0,0,0,0)")
    db.commit()

def save_to_file():
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT * FROM users "
    cursor.execute(sql)
    data = cursor.fetchall()
    str_data = json.dumps(data)
    print(str_data)
    with open('users.txt', 'w') as file:
        file.write(str_data)



@app.route('/')
def homepage():
    try:
        return "hello"
    except Exception as ex:
        print(ex)
        return 'ER'

@app.route('/all')
def homepage2():
    sql = "SELECT * FROM users "
    cursor=get_db().cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    str_data = json.dumps(data)
    print(str_data)
    return str_data

@app.route('/kill/<name>')
def add_kill(name):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_user = "SELECT * FROM users where name='{}'".format(name)
       cursor.execute(sql_user)
       data= cursor.fetchone()
       sql_money = "UPDATE users SET money = {} WHERE name ='{}'".format(data[2] + KILL, name)
       cursor.execute(sql_money)
       db.commit()
       sql = "UPDATE users SET kills = {} WHERE name ='{}'".format(data[5]+1, name)
       cursor.execute(sql)
       db.commit()
       return 'OK'
   except Exception as ex:
       print(ex)
       return 'ER'

@app.route('/check/<name>')
def check(name):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_user = "SELECT * FROM users where name='{}'".format(name)
       cursor.execute(sql_user)
       data= cursor.fetchone()
       if data[2]>=LIFE:
         return 'OK'
       else:
         return 'ER'
   except Exception as ex:
       print(ex)
       return 'ER'

@app.route('/win/<name>')
def win(name):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_user = "SELECT * FROM users where name='{}'".format(name)
       cursor.execute(sql_user)
       data= cursor.fetchone()
       sql_money = "UPDATE users SET money = {} WHERE name ='{}'".format(data[2] + WIN, name)
       cursor.execute(sql_money)
       db.commit()
       sql = "UPDATE users SET wins = {} WHERE name ='{}'".format(data[4]+1, name)
       cursor.execute(sql)
       db.commit()
       return 'OK'
   except Exception as ex:
       print(ex)
       return 'ER'

@app.route('/die/<name>')
def die(name):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_user = "SELECT * FROM users where name='{}'".format(name)
       cursor.execute(sql_user)
       data= cursor.fetchone()
       sql_money = "UPDATE users SET money = {} WHERE name ='{}'".format(data[2] - LIFE, name)
       cursor.execute(sql_money)
       db.commit()
       sql_money = "UPDATE users SET dies = {} WHERE name ='{}'".format(data[6] + 1, name)
       cursor.execute(sql_money)
       db.commit()
       return 'OK'
   except Exception as ex:
       print(ex)
       return 'ER'

@app.route('/getinfo/<name>')
def getinfo(name):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_user = "SELECT * FROM users where name='{}'".format(name)
       cursor.execute(sql_user)
       data= cursor.fetchone()
       if data is None:
           return 'ER'
       return jsonify(data)
   except Exception as ex:
       print(ex)
       return 'ER'

@app.route('/login/<name>&<password>')
def login(name,password):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_user = "SELECT * FROM users where name='{}' and password='{}'".format(name,password)
       cursor.execute(sql_user)
       data= cursor.fetchone()
       if data is None:
           return 'ER'
       return jsonify(data)
   except Exception as ex:
       print(ex)
       return 'ER'

@app.route('/reg/<name>&<password>')
def reg(name,password):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_user = "SELECT * FROM users where name='{}'".format(name)
       cursor.execute(sql_user)
       data= cursor.fetchone()
       if data is None:
           cursor = db.cursor()
           cursor.execute("INSERT INTO users VALUES ('{}', '{}', 0,0,0,0,0)".format(name,password))
           db.commit()
           return 'OK'
       return 'ER'
   except Exception as ex:
       print(ex)
       return 'ER'

def timer_start():
    threading.Timer(120.0, timer_start).start()
    print('start')
    try:
        send()
    except Exception as ex:
        print(ex)

timer_start()
if __name__ == '__main__':

    send()
    app.run()

