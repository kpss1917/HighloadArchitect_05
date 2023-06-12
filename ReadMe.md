Инструкция по запуску
1. при необходимости поменять порты в файлах:</br>
    docker-compose.yml</br>
        ports:</br>
        - '8000:8000'</br>
        ports:</br>
        - '54322:5432'</br>

    HttpServer/db.py</br>
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='postgres', port=5432)</br>

    HttpServer/httpServer.py</br>
        server_address = ('', 8000)</br>

2. запустить </br>
        docker-compose up

3. выполнить скрипт создания таблиц</br>
     SQL/create_tables.sql
 
4. создать пользователя</br>
    http://localhost:8000/user/register?user=1&first_name=Petr&second_name=Petrov&birthdate=2000-02-02&sex=True&biography=hobby&city=Moskow&password=123
5. посмотреть пользователя</br>
    http://localhost:8000/get/1
6. залогиниться</br>
    http://localhost:8000/login?user=1&password=123
