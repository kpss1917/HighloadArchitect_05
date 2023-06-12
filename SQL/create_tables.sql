CREATE SCHEMA IF NOT EXISTS api;
--DROP table IF EXISTS api.Users;
commit;
create table IF NOT EXISTS api.Users(
    id INT GENERATED ALWAYS AS IDENTITY,
    first_name varchar(100),
    second_name varchar(100),
    birthdate date,
    sex BOOLEAN,
    biography VARCHAR(100),
    city varchar(50),
    password varchar(100)
)
;
commit;
/*
delete from api.Users;
commit;
insert into api.Users(first_name, second_name, birthdate, sex, biography, city, password)
values('Ivan', 'Ivanov', '2000-01-01', True, 'хобби', 'город', '855f938d67b52b5a7eb124320a21a139')
RETURNING id
;
commit;

SELECT * FROM api.Users
WHERE id=1 AND password='855f938d67b52b5a7eb124320a21a139'
*/
