import sqlite3
from datetime import datetime


class LocalDB:
    def __init__(self):
        self.conn = sqlite3.connect("tiny_weather_db.sqlite")
        self.cursor = self.conn.cursor()
        cursor = self.cursor
        cursor.execute('''CREATE TABLE IF NOT EXISTS QueryHistory (
                    id INTEGER PRIMARY KEY,
                    short_name TEXT UNIQUE,
                    date TEXT
                )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS WeatherData (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            short_name TEXT UNIQUE,
                            weather_status TEXT,
                            temperature REAL,
                            humidity REAL,
                            date TEXT
                        )''')

        def get_query_history(short_name: str):
            self.cursor.execute("SELECT * FROM QueryHistory WHERE short_name = ?", short_name)
            return self.cursor.fetchone()

        def insert_query_history(short_name, date: datetime):
            self.cursor.execute("INSERT INTO QueryHistory (short_name, date) VALUES (?, ?)",
                                (short_name, date.strftime('%Y-%m-%d').strip()))

        def clear_table(table_name: str):
            self.cursor.execute(f"DELETE FROM {table_name}")
            self.conn.commit()
