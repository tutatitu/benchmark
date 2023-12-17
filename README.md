# Benchmark - DataBase Lab 3
## Основная информация
В лабораторной работе был реализован бенчмарк [4queries](https://medium.unum.cloud/pandas-cudf-modin-arrow-spark-and-a-billion-taxi-rides-f85973bfafd5),
для замера производительности 5 библиотек(`Psycopg2`, `SQLite`,`DuckDB`,`Pandas`,`SQLAlchemy`).
</br>ТЗ и выборки данных можно найти [тут](https://drive.google.com/drive/folders/1usY-4CxLIz_8izBB9uAbg-JQEKSkPMg6).
</br>В качестве языка был выбран `Python` из-за его удобства работы с базами данных и простого синтаксиса.
## Запуск проекта
Для работы с библиотеками необходимо выполнить команду в терминале:
```
pip install -r settings.txt
```
**_<ins>Для работы с psycopg2 версия python должна быть меньше 3.10</ins>_**

</br>Далее необходимо установить [папку](https://drive.google.com/drive/folders/1XUNdFTeCnMS-xKpYOBzKa55ifRUSzXE4?usp=sharing) с базой данных в проект.
## Библиотеки
### Psycorg2
Предоставляет низкоуровневый доступ к базе данных, позволяя выполнять SQL-запросы, управлять транзакциями и работать с различными типами данных. Psycopg2 обеспечивает высокую производительность и надежность при взаимодействии с PostgreSQL и широко используется в различных проектах.

</br>Использование:
```py
import psycopg2

conn = psycopg2.connect(database="dbname", user="username", password="password", host="hostname", port="portnum")  # соединение с базой данных
# в нашем случае - psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")

cursor = conn.cursor() 
cursor.execute("SQL-query") # выполнение SQL запроса
conn.commit() # запись в базу данных
cursor.close() 
conn.close()
```
### SQLite
SQLite – это компактная, встраиваемая реляционная база данных, которая не требует отдельного сервера для своей работы. Она поддерживает стандартный набор SQL команд и обладает высокой производительностью. SQLite хранит всю базу данных в одном файле, что делает ее удобной для встраивания в приложения.

</br>Использование:
```py
import sqlite3

conn = sqlite3.connect("dbname.db")  # соединение с базой данных, в нашем случае - connect("db/postgres.db")

cursor = conn.cursor() 
cursor.execute("SQL-query") # выполнение SQL запроса
conn.commit() # запись в базу данных
cursor.close() 
conn.close()
```
### DuckDB
DuckDB - это аналитическая база данных с открытым исходным кодом, которая разрабатывается для эффективной обработки аналитических запросов. Она предназначена для использования в приложениях, требующих быстрых запросов и аналитики на больших объемах данных. DuckDB поддерживает стандарт SQL и может работать как в режиме встроенной библиотеки, так и в режиме сервера. Основные принципы проектирования DuckDB включают высокую производительность, низкую задержку запросов и малый объем памяти, необходимый для работы.

</br>Использование:
```py
import duckdb

conn = sqlite3.connect("dbname.db")  # соединение с базой данных, также поддерживается соединение с "dbname.duckdb"

cursor = conn.cursor() 
cursor.execute("SQL-query") # выполнение SQL запроса
cursor.close() 
conn.close()
```
### Pandas
Библиотека Pandas в Python предоставляет мощные инструменты для работы с данными в виде двумерных таблиц, известных как DataFrame. В контексте баз данных, pandas может использоваться для загрузки данных из различных источников, включая реляционные базы данных через SQL-запросы. Она обеспечивает удобные методы для фильтрации, агрегации и манипуляций с данными, что делает ее популярным выбором для анализа и обработки данных из баз данных в научных и коммерческих приложениях.

</br>Использование:
```py
import psycopg2
import sqlite3
import duckdb
import pandas as pd
from sqlalchemy import create_engine

# 1 способ
conn = sqlite3.connect("dbname.db") # также можем подключиться с помощью psycorg2 или duckdb

# 2 способ
conn = create_engine("dialect+driver//username:password@hostname:portnum/dbname")
# или
conn = create_engine('sqlite:///dbname.db')

pd.read_sql("SQL query", conn) # выполнение SQL запроса
```
### SQLAlchemy
Библиотека SQLAlchemy в Python представляет собой мощный инструмент для взаимодействия с реляционными базами данных. Она предоставляет высокоуровневый API для создания, управления и выполнения SQL-запросов в базах данных, а также абстрагирует детали работы с различными системами управления базами данных (СУБД). SQLAlchemy позволяет создавать объектные отображения, что упрощает работу с данными, а также обеспечивает мощные средства для создания сложных SQL-выражений. Эта библиотека часто используется при разработке веб-приложений и других проектов, где требуется эффективное взаимодействие с базами данных.

</br>Использование:
```py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

conn = create_engine("dialect+driver//username:password@hostname:portnum/dbname")
# или
conn = create_engine('sqlite:///dbname.db')

session = sessionmaker(bind=conn)()
session.execute(text("SQL-query")) # SQLalchemy работает только с text в execute
session.close()
engine.dispose()
