from flask import Flask, jsonify
import psycopg2
from psycopg2 import sql


app = Flask(__name__)

conn = psycopg2.connect(dbname='mydb', user='myuser',
                        password='12345678', host='myhost.com')

@app.route('/')
def homepage():
    return "hello"


@app.route('/get_id')
def get_id():
   try:
       with conn.cursor() as cursor:
           conn.autocommit = True

           sql_select = "SELECT TASK_ID FROM state_table WHERE STATE=1"
           cursor.execute(sql_select)
           task_id= cursor.fetchone()

           sql_update = "UPDATE state_table SET state=2 WHERE TASK_ID={}".format(task_id[0])
           cursor.execute(sql_update)
           return jsonify(id=task_id[0])
   except Exception as ex:
       print(ex)


@app.route('/close_id/<id>')
def close_id(id):
    try:
        with conn.cursor() as cursor:
            conn.autocommit = True
            sql_update = "UPDATE state_table SET state=3 WHERE TASK_ID={}".format(id)
            cursor.execute(sql_update)
            return 'ok'
    except Exception as ex:
        print(ex)



@app.route('/clean')
def clean():
    try:

        with conn.cursor() as cursor:
            conn.autocommit = True

            clean = sql.SQL('TRUNCATE table state_table')
            cursor.execute(clean)

        list_data=[]
        for i in range(1, 40000):
            list_data.append((i,1))
        with conn.cursor() as cursor:
            conn.autocommit = True
            insert = sql.SQL('INSERT INTO state_table (task_id,state) VALUES {}').format(
                sql.SQL(',').join(map(sql.Literal, list_data))
            )

            cursor.execute(insert)
    except Exception as ex:
        print(ex)
    return 'ok'


if __name__ == '__main__':
    app.run()

