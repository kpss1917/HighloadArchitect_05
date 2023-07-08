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

SELECT * FROM api.Users limit 100
WHERE id=1 AND password='855f938d67b52b5a7eb124320a21a139'

explain SELECT * FROM api.Users WHERE first_name LIKE 'Абрамов%' AND second_name LIKE 'А%' ORDER BY id 
explain SELECT * FROM api.Users WHERE first_name LIKE 'Абрамов%' 
explain SELECT * FROM api.Users WHERE first_name LIKE 'Абрамов%'
first_name=Абрамов%&second_name=А%

DROP INDEX IF EXISTS IX_api_Users_first_name_second_name 
CREATE INDEX IF NOT EXISTS IX_api_Users_first_name_second_name ON api.Users(first_name  text_pattern_ops, second_name  text_pattern_ops)
*/
select CURRENT_DATE - INTERVAL '2 year'

drop table if exists api.Users_tmp;
commit;

create table IF NOT EXISTS api.Users_tmp(
    --id INT GENERATED ALWAYS AS IDENTITY,
    FIO varchar(200),
    age int,
    city varchar(50)
)
;
commit;

create table IF NOT EXISTS api.Users_tmp2(
    --id INT GENERATED ALWAYS AS IDENTITY,
    age int,
    city varchar(50),
    first_name varchar(100),
    second_name varchar(100)

)
;
commit;

--select setting from pg_settings where name = 'data_directory';

--COPY api.Users_tmp FROM '/home/igor/Work/GIT/HighloadArchitect_05/data/people.csv' DELIMITER ',' CSV;
--commit;

copy api.users_tmp (FIO, age, city) FROM '/home/igor/Work/GIT/HighloadArchitect_05/data/people.csv' DELIMITER ',' CSV;

copy api.users_tmp (fio, age, city) FROM '/home/igor/Work/GIT/HighloadArchitect_05/data/people.csv' DELIMITER ',' CSV 

insert into api.users(first_name, second_name, birthdate, city)
select split_part(fio, ' ', 1) as first_name,
       split_part(fio, ' ', 2) as second_name,
       CURRENT_DATE - (cast(age as varchar(5))||' year')::INTERVAL as birthdate,
       city
from api.users_tmp

select count(*) from api.users_tmp
select split()* from api.users_tmp limit 100
SELECT split_part('Абрамов Лев', ' ', 1), split_part('Абрамов Лев', ' ', 2);



