import configparser
from pathlib import Path
from collections import namedtuple
from typing import List, NamedTuple, Tuple
from datetime import date, datetime

import sqlite3

import pandas as pd

DEFAULT_DATE_FORMAT = '%d-%m-%Y'
DEFAULT_DB_FILE_PATH = Path.joinpath(Path.cwd(), "_pyClocker", "worksessions.db")
SCHEMA_FILE_PATH = Path.joinpath(Path.cwd(), "_pyClocker", "schema.sql")

class WorkSession(NamedTuple):
    activity: str
    start_time: float
    stop_time: float

class WorkSessionInfo(NamedTuple):
    id: int
    date: str
    activity: str
    start_time: float
    stop_time: float

class DailyWorkHours(NamedTuple):
    date: str
    activity: str
    hours: float

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the pyClocker database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path):
    """Create the pyClocker database."""
    connection = sqlite3.connect(db_path)
    with open(SCHEMA_FILE_PATH, 'r') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def get_time_spent_on_work_for_today(self) -> List[WorkSession]:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        work_sessions = cursor.execute('SELECT activity, start_time, stop_time FROM worksessions where date=? AND stop_time is NOT NULL;', (date.today().strftime(DEFAULT_DATE_FORMAT),)).fetchall()
        work_sessions = [WorkSession(activity=activity, start_time=start, stop_time=stop) for activity, start, stop in work_sessions]
        connection.close()
        return work_sessions
    
    def get_current_work_session(self) -> WorkSessionInfo:
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        latest_work_session = cursor.execute('SELECT * FROM worksessions where date=? order by start_time desc limit 1;', (date.today().strftime(DEFAULT_DATE_FORMAT),)).fetchone()
        if latest_work_session:
            latest_work_session = WorkSessionInfo(*latest_work_session)
        connection.close()
        return latest_work_session

    def create_work_session(self, activity):
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO worksessions(date, activity, start_time) values(?, ?, ?);', (date.today().strftime(DEFAULT_DATE_FORMAT), activity, datetime.now().timestamp()))
        connection.commit()
        connection.close()

    def end_work_session(self, id):
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute('UPDATE worksessions SET stop_time=? where id=?;', (datetime.now().timestamp(), id))
        connection.commit()
        connection.close()

    def get_daily_time_spent_on_work(self) -> Tuple[pd.DataFrame, List[str]]:
        connection = sqlite3.connect(self._db_path)
        df = pd.read_sql_query("SELECT date, activity, ROUND(SUM(stop_time-start_time)*1.0/3600, 2) as hours FROM worksessions where stop_time is not null GROUP BY date, activity;", connection)
        df['date'] = pd.to_datetime(df['date'], format=DEFAULT_DATE_FORMAT)

        cursor = connection.cursor()
        activities = cursor.execute('SELECT distinct activity FROM worksessions;').fetchall()

        connection.close()
        
        return df, [activity[0] for activity in activities]