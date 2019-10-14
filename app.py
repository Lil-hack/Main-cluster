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
            sql_get = "SELECT ID FROM cluster WHERE STATE=1"
            cursor.execute(sql_get)
            count = cursor.fetchone()
            sql_update = "UPDATE cluster SET state=2 WHERE ID={}".format(count[0])
            cursor.execute(sql_update)
            return jsonify(id=count[0])
    except Exception as ex:
        print(ex)

@app.route('/close_id/<id>')
def close_id(id):
    try:
        with conn.cursor() as cursor:
            conn.autocommit = True
            sql_update = "UPDATE cluster SET state=3 WHERE ID={}".format(id)
            cursor.execute(sql_update)
            return 'ok'
    except Exception as ex:
        print(ex)



@app.route('/clean')
def clean():
    try:
        with conn.cursor() as cursor:
            conn.autocommit = True

            clean = sql.SQL('TRUNCATE table cluster')
            cursor.execute(clean)
        list_data=[]
        for i in range(1, 40000):
            list_data.append((i,1))
        with conn.cursor() as cursor:
            conn.autocommit = True
            insert = sql.SQL('INSERT INTO cluster (id,state) VALUES {}').format(
                sql.SQL(',').join(map(sql.Literal, list_data))
            )

            cursor.execute(insert)
    except Exception as ex:
        print(ex)
    return 'ok'


if __name__ == '__main__':
    app.run()

