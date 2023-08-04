import sqlite3
from datetime import datetime, timedelta
from typing import Union

from weather_api_caller.data.WeatherData import WeatherData


def cast_hour(time: datetime):
    return time.strftime('%Y-%m-%d %H:%M').strip()


def cast_from_db(raw) -> WeatherData:
    _, city_name, country_name, short_name, weather_status, temperature, humidity, date = raw
    date = datetime.strptime(date, '%Y-%m-%d %H:%M')
    return WeatherData(city_name, country_name, short_name,
                       weather_status, temperature, humidity, date)


class LocalDB:
    def __init__(self, db_filename: str = "tiny_weather_db"):
        self.conn = sqlite3.connect(f"{db_filename}.sqlite")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS QueryHistory (
                    id INTEGER PRIMARY KEY,
                    city_name TEXT,
                    country_name TEXT,
                    date TEXT,
                    weather_status TEXT,
                    UNIQUE(city_name, country_name, date)
                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS WeatherData (
                            id INTEGER PRIMARY KEY,
                            city_name TEXT,
                            country_name TEXT,
                            short_name TEXT,
                            weather_status TEXT,
                            temperature REAL,
                            humidity REAL,
                            date TEXT,
                            UNIQUE(city_name, country_name)
                        )''')
        self.query_history = "QueryHistory"
        self.weather_data = "WeatherData"

    def get_query_history(self, city_name: str) -> tuple[datetime, str] | None:
        self.cursor.execute("SELECT date, weather_status FROM QueryHistory WHERE city_name = ?", (city_name,))
        raw_date = self.cursor.fetchone()
        if raw_date:
            return datetime.strptime(raw_date[0], '%Y-%m-%d %H:%M'), raw_date[1]
        return None

    def insert_query_history(self, city_name, date: datetime, weather_status: str, country_name=""):
        date = date.replace(minute=0, second=0, microsecond=0)

        stored = self.get_query_history(city_name)
        if stored:
            stored_date, _ = stored
            if stored_date == date:
                return
        self.cursor.execute("INSERT INTO QueryHistory (city_name, date, weather_status, country_name) VALUES (?, ?, "
                            "?, ?)",
                            (city_name, date.strftime('%Y-%m-%d %H:%M').strip(), weather_status,country_name))
        self.conn.commit()

    def get_history_date(self):
        self.cursor.execute("SELECT date FROM QueryHistory LIMIT 1")
        date = self.cursor.fetchone()
        if date:
            return datetime.strptime(date[0], '%Y-%m-%d %H:%M')
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
        date = data.date
        next_hour = date.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        self.cursor.execute("SELECT 1 FROM WeatherData WHERE city_name = ? AND date >= ? AND date < ? AND "
                            "country_name = ?",
                            (data.city_name, cast_hour(date), cast_hour(next_hour), data.country_name))
        return self.cursor.fetchone() is not None

    def insert_weather(self, data: Union[WeatherData, list[WeatherData]]):
        if isinstance(data, WeatherData):
            data.date = data.date.replace(minute=0, second=0, microsecond=0)
            if not self.check_if_stored_weather(data):
                values = list(vars(data).values())
                values[-1] = values[-1].strftime('%Y-%m-%d %H:%M').strip()
                self.cursor.execute(
                    "INSERT INTO WeatherData "
                    "(city_name, country_name, short_name, weather_status, temperature, humidity, date) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (tuple(values)))
        else:
            for weather in data:
                self.insert_weather(weather)
        self.conn.commit()

    def get_weathers(self, city_name: str) -> tuple[list[WeatherData], WeatherData]:
        ref = self.cursor.execute(f"SELECT * FROM {self.weather_data} WHERE  city_name = ?", (city_name,))
        ref = cast_from_db(ref.fetchone())
        self.cursor.execute(f"SELECT * FROM {self.weather_data} WHERE weather_status = ?", (ref.weather_status,))
        weather_data = []
        for raw in self.cursor.fetchall():
            weather_data.append(cast_from_db(raw))

        return weather_data, ref
