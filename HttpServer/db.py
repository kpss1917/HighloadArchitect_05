import psycopg2
from psycopg2 import sql
from contextlib import closing
import hashlib

class db_api():
    def conn(self):
        #conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost', port=5432)
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='postgres', port=5432)
        
        return conn

    def login(self, user_id: int, password: str):
        connection = self.conn()
        pwd = str(hashlib.md5(password.encode('utf-8')).hexdigest())
        with(closing(connection)) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM api.Users WHERE id={} AND password='{}'".format(user_id, pwd))
                ret = cursor.fetchone()
        return ret
    def user_register(self, user_id, first_name, second_name, birthdate,
                                  sex, biography, city, password):
        connection = self.conn()
        pwd = str(hashlib.md5(password.encode('utf-8')).hexdigest())
        with(closing(connection)) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                values = [
                    (first_name, second_name, birthdate, sex, biography, city, pwd),
                ]
                insert = sql.SQL('INSERT INTO api.Users (first_name, second_name, birthdate, sex, '
                                 'biography, city, password) VALUES {} RETURNING id').format(
                    sql.SQL(',').join(map(sql.Literal, values))
                )
                cursor.execute(insert)
                ret = cursor.fetchone()
        return ret
    def user_get(self, user_id: int):
        connection = self.conn()
        with(closing(connection)) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM api.Users WHERE id={}'.format(user_id))
                ret = cursor.fetchone()
        return ret
