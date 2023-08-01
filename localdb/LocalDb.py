import sqlite3
from datetime import datetime
from typing import Union

from weather_api_caller.data.WeatherData import WeatherData


def cast_from_db(raw) -> WeatherData:
    _, city_name, country_name, short_name, weather_status, temperature, humidity, date = raw
    date = datetime.strptime(date, '%Y-%m-%d')
    return WeatherData(city_name, country_name, short_name,
                       weather_status, temperature, humidity, date)


class LocalDB:
    def __init__(self, db_filename: str = "tiny_weather_db"):
        self.conn = sqlite3.connect(f"{db_filename}.sqlite")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS QueryHistory (
                    id INTEGER PRIMARY KEY,
                    short_name TEXT UNIQUE,
                    date TEXT,
                    weather_status TEXT
                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS WeatherData (
                            id INTEGER PRIMARY KEY,
                            city_name TEXT,
                            country_name TEXT,
                            short_name TEXT UNIQUE,
                            weather_status TEXT,
                            temperature REAL,
                            humidity REAL,
                            date TEXT
                        )''')
        self.query_history = "QueryHistory"
        self.weather_data = "WeatherData"

    def get_query_history(self, short_name: str) -> tuple[datetime, str] | None:
        self.cursor.execute("SELECT date, weather_status FROM QueryHistory WHERE short_name = ?", (short_name,))
        raw_date = self.cursor.fetchone()
        if raw_date:
            return datetime.strptime(raw_date[0], '%Y-%m-%d'), raw_date[1]
        return None

    def insert_query_history(self, short_name, date: datetime, weather_status: str):
        self.cursor.execute("INSERT INTO QueryHistory (short_name, date, weather_status) VALUES (?, ?, ?)",
                            (short_name, date.strftime('%Y-%m-%d').strip(), weather_status))
        self.conn.commit()

    def get_history_date(self):
        self.cursor.execute("SELECT date FROM QueryHistory LIMIT 1")
        date = self.cursor.fetchone()
        if date:
            return datetime.strptime(date[0], '%Y-%m-%d')
        return

    def clear_table(self, table_name: str):
        self.cursor.execute(f"DELETE FROM {table_name}")
        self.conn.commit()

    def table_count(self, table_name: str):
        return self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    def get_history_count(self):
        return self.table_count(self.query_history)

    def clear_history(self):
        return self.clear_table(self.query_history)

    def get_weather_count(self):
        return self.table_count(self.weather_data)

    def clear_weather(self):
        return self.clear_table(self.weather_data)

    def check_if_stored_weather(self, data: WeatherData):
        self.cursor.execute("SELECT 1 FROM WeatherData WHERE short_name = ? AND date = ?",
                            (data.short_name, data.date.strftime('%Y-%m-%d').strip()))
        return self.cursor.fetchone() is not None

    def insert_weather(self, data: Union[WeatherData, list[WeatherData]]):
        if isinstance(data, WeatherData):
            if not self.check_if_stored_weather(data):
                values = list(vars(data).values())
                values[-1] = values[-1].strftime('%Y-%m-%d').strip()
                self.cursor.execute(
                    "INSERT INTO WeatherData "
                    "(city_name, country_name, short_name, weather_status, temperature, humidity, date) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (tuple(values)))
        else:
            for weather in data:
                self.insert_weather(weather)
        self.conn.commit()

    def get_weathers(self, short_name: str, weather_status: str) -> tuple[list[WeatherData], WeatherData]:
        self.cursor.execute(f"SELECT * FROM {self.weather_data} WHERE weather_status = ?", (weather_status,))
        weather_data = []
        for raw in self.cursor.fetchall():
            weather_data.append(cast_from_db(raw))
        ref = self.cursor.execute(f"SELECT * FROM {self.weather_data} WHERE  short_name = ? AND weather_status = ?",
                                  (short_name, weather_status))
        return weather_data, cast_from_db(ref.fetchone())
