import json
import threading
import os
import time
from multiprocessing import Process, Manager

from flask import Flask, jsonify, g, request, current_app
import sqlite3
import requests

try:
    from ssh_client import send, get
except:
    print('no paramilo')
app = Flask(__name__)

file_name='minecraft.db'
path = os.path.dirname(os.path.abspath(__file__))+'/'

LIFE=10
KILL=5
WIN=50

TOKEN='UFSv7R04U9USUNNNl7WyPTffdSw2TzlvC6znuTnHl68rpZgpUgeN0H358S0Z'

ERROR={"status":"Error"}
OK={"status":"Ok"}
p=9
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

@app.route('/sql/<sql>')
def sql(sql):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql.replace('&',' '))
        db.commit()
        return "OK"
    except Exception as ex:
        print(ex)
        return ERROR



@app.route('/')
def homepage():
    try:
        return "hello"
    except Exception as ex:
        print(ex)
        return ERROR

@app.route('/all')
def homepage2():
    sql = "SELECT * FROM users "
    cursor=get_db().cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    str_data = json.dumps(db_to_json(data))

    return str_data

@app.route('/kill/<name>')
def add_kill(name):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_money = "UPDATE users SET money = money + {} WHERE name ='{}'".format(KILL, name)
       cursor.execute(sql_money)
       db.commit()
       sql = "UPDATE users SET kills = kills + 1 WHERE name ='{}'".format(name)
       cursor.execute(sql)
       db.commit()
       return OK
   except Exception as ex:
       print(ex)
       return ERROR

@app.route('/check/<name>')
def check(name):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_user = "SELECT * FROM users where name='{}'".format(name)
       cursor.execute(sql_user)
       data= cursor.fetchone()
       if data[2]>=LIFE:
         return OK
       else:
         return ERROR
   except Exception as ex:
       print(ex)
       return ERROR

@app.route('/win/<name>&<money>')
def win(name,money):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_money = "UPDATE users SET money = money + {} WHERE name ='{}'".format(int(money), name)
       cursor.execute(sql_money)
       db.commit()
       sql = "UPDATE users SET wins = wins + 1 WHERE name ='{}'".format(name)
       cursor.execute(sql)
       db.commit()
       return OK
   except Exception as ex:
       print(ex)
       return ERROR

@app.route('/die/<name>')
def die(name):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_money = "UPDATE users SET money = money + {} WHERE name ='{}'".format(LIFE, name)
       cursor.execute(sql_money)
       db.commit()
       sql_die = "UPDATE users SET dies = dies + 1 WHERE name ='{}'".format( name)
       cursor.execute(sql_die)
       db.commit()
       return OK
   except Exception as ex:
       print(ex)
       return ERROR

@app.route('/getinfo/')
def getinfo():
   list_user=[]
   try:
       for i in range(1,30):
          user=request.args.get(f'name{i}')
          if user is not None:
            list_user.insert(i-1,user)
            print(user)
          else:
              break

       db = get_db()
       cursor = db.cursor()
       sql_user = "SELECT * FROM users where "
       list_size=len(list_user)
       for i in range(0,list_size):
           if i!=list_size-1:
                sql_user=sql_user+"name='{}' or ".format(list_user[i])
           else:
               sql_user = sql_user + "name='{}' ".format(list_user[i])
       print(sql_user)
       cursor.execute(sql_user)
       data= cursor.fetchall()

       if data is None:
           return ERROR
       str_data = json.dumps(db_to_json(data))
       return str_data
   except Exception as ex:
       print(ex)
       return ERROR

@app.route('/login/<name>&<password>')
def login(name,password):
   try:
       db = get_db()
       cursor = db.cursor()
       sql_user = "SELECT * FROM users where name='{}' and password='{}'".format(name,password)
       cursor.execute(sql_user)
       data= cursor.fetchone()
       if data is None:
           return ERROR
       str_data = json.dumps(db_to_json([data]))
       return str_data
   except Exception as ex:
       print(ex)
       return ERROR

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
           return OK
       return ERROR
   except Exception as ex:
       print(ex)
       return ERROR


def db_to_json(data):
    json_list = []
    json_output = {'users': json_list}

    for row in data:
        json_dict = {'name': row[0], 'password': row[1], 'money': row[2], 'life': row[3], 'wins': row[4], 'kills': row[5], 'dies': row[6]}
        json_list.append(json_dict)
    return json_output

def timer_transac():
    threading.Timer(60.0, timer_transac).start()
    try:
        with open('pay.json') as f:
            pay = json.load(f)
        # print(pay)


        response = requests.get('https://donatepay.ru/api/v1/transactions?access_token={}'.format(TOKEN))
        json_pay=response.json()
        if json_pay['status'] != 'success':
            return
        print(json_pay)
        if pay['pay_id'] == 0:
            last_id = json_pay['data'][0]['id']
        else:
            last_id=pay['pay_id']

        for data in json_pay['data']:
            if data['id']==last_id:
                print('end')
                break
            else:
                with app.app_context():
                    if data['comment']=='':
                        db = get_db()
                        cursor = db.cursor()
                        sql_money = "UPDATE users SET money = money + {} WHERE name ='{}'".format(int(float(data['sum'])), data['what'])
                        cursor.execute(sql_money)
                        db.commit()
                    else:
                        db = get_db()
                        cursor = db.cursor()
                        sql_money = "UPDATE users SET money = money + {} WHERE name ='{}'".format(
                            int(float(data['sum'])), data['comment'])
                        cursor.execute(sql_money)
                        db.commit()


        to_json = {'pay_id': json_pay['data'][0]['id']}
        with open('pay.json', 'w') as f:
            json.dump(to_json, f)

    except Exception as ex:
        print(ex)

def timer_start():
    threading.Timer(120.0, timer_start).start()
    print('start')
    try:
        send()
    except Exception as ex:
        print(ex)
        get()

get()
threading.Timer(120.0, timer_start).start()
threading.Timer(25.0, timer_transac).start()
# timer_transac()
# timer_start()
if __name__ == '__main__':

    app.run()


