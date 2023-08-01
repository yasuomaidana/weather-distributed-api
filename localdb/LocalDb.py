import sqlite3
from datetime import datetime


class LocalDB:
    def __init__(self, db_filename: str = "tiny_weather_db"):
        self.conn = sqlite3.connect(f"{db_filename}.sqlite")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS QueryHistory (
                    id INTEGER PRIMARY KEY,
                    short_name TEXT UNIQUE,
                    date TEXT
                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS WeatherData (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            short_name TEXT UNIQUE,
                            weather_status TEXT,
                            temperature REAL,
                            humidity REAL,
                            date TEXT
                        )''')
        self.query_history = "QueryHistory"
        self.weather_data = "WeatherData"

    def get_query_history(self, short_name: str) -> datetime | None:
        self.cursor.execute("SELECT date FROM QueryHistory WHERE short_name = ?", (short_name, ))
        raw_date = self.cursor.fetchone()
        if raw_date:
            return datetime.strptime(raw_date[0], '%Y-%m-%d')
        return None

    def insert_query_history(self, short_name, date: datetime):
        self.cursor.execute("INSERT INTO QueryHistory (short_name, date) VALUES (?, ?)",
                            (short_name, date.strftime('%Y-%m-%d').strip()))

    def clear_table(self, table_name: str):
        self.cursor.execute(f"DELETE FROM {table_name}")
        self.conn.commit()

    def table_count(self, table_name: str):
        return self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    def get_history_count(self):
        return self.table_count(self.query_history)

    def clear_history(self):
        return self.clear_table(self.query_history)
