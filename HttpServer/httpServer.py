from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse, parse_qs
import re
from db import db_api
from random import randint

sessions = {}
def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
  server_address = ('', 8000)
  httpd = server_class(server_address, handler_class)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()

class HttpGetHandler(BaseHTTPRequestHandler):
    #"""Обработчик с реализованным методом do_GET."""
    sid: str = ''
    cookie = None
    def generate_sid(self):
        return "".join(str(randint(1, 9)) for _ in range(100))

    def parse_cookies(self, cookie_list):
        return dict(((c.split("=")) for c in cookie_list.split(";"))) if cookie_list else {}
    def ret200(self, title, body):
        sid = self.sid
        user = ''
        if sid:
            user = sessions[sid]
        else:
            user = 'Not Autorised'
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        if self.cookie:
            self.send_header('Set-Cookie', self.cookie)  # Addition
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode())
        self.wfile.write('<title>{}</title></head>'.format(title).encode())
        self.wfile.write('<body><table><tr><td>{}</td><td>Login as {}</td></tr></table></body></html>' \
                         .format(body, user).encode())

    def ret404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        if self.cookie:
            self.send_header('Set-Cookie', self.cookie)  # Addition
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode())
        self.wfile.write('<title>"Анкета не найдена"</title></head>'.encode())
        self.wfile.write('<body>Анкета не найдена</body></html>'.encode())

    def do_Login(self, user_id: int, password: str):
        db = db_api()
        user = db.login(user_id, password)
        if user:
            self.sid = self.generate_sid()
            self.cookie = "sid={}".format(self.sid)
            sessions[self.sid] = {user_id, user[1], user[2]}
            self.ret200(title='Успешная авторизация', body=f'пользователь={user}')
        else:
            self.ret404()
    def do_user_register(self, user_id, first_name, second_name, birthdate,
                                  sex, biography, city, password):
        db = db_api()
        user = db.user_register(user_id, first_name, second_name, birthdate,
                                  sex, biography, city, password)
        if user:
            self.ret200(title='Успешное добавление анкеты пользователя', body=f'пользователь ID={user} добавлен')
        else:
            self.ret404()
    def do_user_get(self, user_id=0):
        db = db_api()
        user = db.user_get(user_id)
        if user:
            self.ret200(title='Успешное получение анкеты пользователя', body=f'пользователь={user}')
        else:
            self.ret404()

    def do_user_search(self, first_name, second_name):
        db = db_api()
        users = db.user_search(first_name, second_name)
        if users:
            self.ret200(title='Результат поиска пользователей', body=f'{users}')
        else:
            self.ret404()
            
    def do_GET(self):
        parsed_url = urlparse(self.path)
        res = re.match(r"(/user/get/)(\d+)", self.path)
        path = parsed_url.path
        user_id = 0


        cookies = self.parse_cookies(self.headers["Cookie"])
        if "sid" in cookies:
            self.sid = cookies["sid"] if (cookies["sid"] in sessions) else False
        else:
            self.sid = False

        if res:
            path = res.group(1)
            user_id = res.group(2)
        if path=='/login':
            #http://localhost:8000/login?user=5&password=321
            user_id = parse_qs(parsed_url.query)['user'][0]
            password = parse_qs(parsed_url.query)['password'][0]
            self.do_Login(user_id=user_id, password=password)
        elif path=='/user/register':
            #http://localhost:8000/user/register?user=1&first_name=Petr&second_name=Petrov&birthdate=2000-02-02&sex=True&biography=hobby&city=Moskow&password=123
            user_id = parse_qs(parsed_url.query)['user'][0]
            password = parse_qs(parsed_url.query)['password'][0]
            first_name = parse_qs(parsed_url.query)['first_name'][0]
            second_name = parse_qs(parsed_url.query)['second_name'][0]
            birthdate = parse_qs(parsed_url.query)['birthdate'][0]
            sex = parse_qs(parsed_url.query)['sex'][0]
            biography = parse_qs(parsed_url.query)['biography'][0]
            city = parse_qs(parsed_url.query)['city'][0]
            password = parse_qs(parsed_url.query)['password'][0]

            self.do_user_register(user_id, first_name, second_name, birthdate,
                                  sex, biography, city, password)
        elif path=='/user/get/':
            #http://localhost:8000/user/get/10
            self.do_user_get(user_id)
        elif path=='/user/search':
            #http://localhost:8000/user/search?first_name=Абрамов%&second_name=A%
            first_name = parse_qs(parsed_url.query)['first_name'][0]
            second_name = parse_qs(parsed_url.query)['second_name'][0]
            self.do_user_search(first_name, second_name)
            
        else:
            self.ret404()


if __name__ == '__main__':
    run(handler_class=HttpGetHandler)


