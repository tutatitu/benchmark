import time
import psycopg2
import sqlite3
import duckdb
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

tests = 15
library = ["Postgres", "SQLite", "DuckDB", "Pandas", "SQLAlchemy"]
Postgres_conn = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="localhost", port="5432")
duckdb.execute("INSTALL sqlite")
DuckDB_conn = duckdb.connect("db/postgres.db")
SQLite_conn = sqlite3.connect("db/postgres.db")
engine = create_engine('sqlite:///db/postgres.db')
SQLAlchemy_conn = sessionmaker(bind=engine)()

conn = [Postgres_conn.cursor(), SQLite_conn.cursor(), DuckDB_conn.cursor(), SQLite_conn, SQLAlchemy_conn]
Postgress_query = ["SELECT cab_type, count(*) FROM trips GROUP BY 1;",
                   "SELECT passenger_count, avg(total_amount) FROM trips GROUP BY 1;",
                   "SELECT passenger_count, extract(year from pickup_datetime), count(*) FROM trips GROUP BY 1, 2;",
                   "SELECT passenger_count, extract(year from pickup_datetime), round(trip_distance), count(*) FROM trips GROUP BY 1, 2, 3 ORDER BY 2, 4 desc;"]
SQLite_query = ["SELECT cab_type, count(*) FROM trips GROUP BY 1;",
                "SELECT passenger_count, avg(total_amount) FROM trips GROUP BY 1;",
                "SELECT passenger_count, strftime('%Y', pickup_datetime), count(*) FROM trips GROUP BY 1, 2;",
                "SELECT passenger_count, strftime('%Y', pickup_datetime), round(trip_distance), count(*) FROM trips GROUP BY 1, 2, 3 ORDER BY 2, 4 desc;"]
# SQLAlchemy воспринимает только text
SQLite_query_text = [text("SELECT cab_type, count(*) FROM trips GROUP BY 1;"),
                     text("SELECT passenger_count, avg(total_amount) FROM trips GROUP BY 1;"),
                     text("SELECT passenger_count, strftime('%Y', pickup_datetime), count(*) FROM trips GROUP BY 1, 2;"),
                     text("SELECT passenger_count, strftime('%Y', pickup_datetime), round(trip_distance), count(*) FROM trips GROUP BY 1, 2, 3 ORDER BY 2, 4 desc;")]
query = [Postgress_query, SQLite_query, SQLite_query, SQLite_query, SQLite_query_text]

answer_table = [[0] * 4 for i in range(5)]
for library_id in range(len(library)):
    for query_id in range(4):
        times = []
        for _ in range(tests):
            if library_id == 3:
                start = time.time()
                pd.read_sql(query[library_id][query_id], conn[library_id])
                elapsed_time = time.time() - start
                times.append(elapsed_time)
                continue
            start = time.time()
            conn[library_id].execute(query[library_id][query_id])
            elapsed_time = time.time() - start
            times.append(elapsed_time)
        sorted(times)
        answer_table[library_id][query_id] = times[tests // 2]
        if library_id == 0:
            answer_table[library_id][query_id] *= 18.32  # разница между big и tiny
        answer_table[library_id][query_id] = round(answer_table[library_id][query_id], 2)
for query_id in range(4):
    print("           ", str(query_id + 1) + "_query", end='')
print()
for library_id in range(len(library)):
    print(library[library_id], end=' ')
    for _ in range(12 - len(library[library_id])):
        print(' ', end='')
    for query_id in range(4):
        print(answer_table[library_id][query_id], end='               ')
    print()