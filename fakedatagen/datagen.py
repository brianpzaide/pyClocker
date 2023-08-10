from datetime import datetime
from pathlib import Path
import random 
import sqlite3

DEFAULT_DATE_FORMAT = '%d-%m-%Y'
DEFAULT_DB_FILE_PATH = Path.joinpath(Path.cwd(), "worksessions.db")
DEFAULT_SCHEMA_FILE_PATH = Path.joinpath(Path.cwd(), "schema.sql")

def init_database():
    connection = sqlite3.connect(DEFAULT_DB_FILE_PATH)
    with open(DEFAULT_SCHEMA_FILE_PATH, 'r') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

def create_work_session(_date, activity, start_time, stop_time):
        connection = sqlite3.connect(DEFAULT_DB_FILE_PATH)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO worksessions(date, activity, start_time, stop_time) values(?, ?, ?, ?);', (_date, activity, start_time, stop_time))
        connection.commit()
        connection.close()

def generate_fake_worksessions():
    activities = ["volunteer", "writing"]
    for i in [2021, 2022]:
        for m, d in ((1,31),(2,28),(3,31),(4,30),(5,31),(6,30),(7,31),(8,31),(9,30),(10,31),(11,30),(12,31)):
            for _d in range(1, d+1):
                start_time = datetime(year=i, month=m, day=_d).timestamp()
                _date = datetime(year=i, month=m, day=_d).strftime(DEFAULT_DATE_FORMAT)
                hours_worked = 0
                hours_tobe_worked = random.randint(4, 10)

                while hours_worked < hours_tobe_worked:
                    session_hrs = random.randint(0, 5)
                    if session_hrs != 0:
                        create_work_session(_date, random.choice(activities), start_time, start_time+(session_hrs*3600))
                        start_time = start_time+(session_hrs*3600)
                        hours_worked += session_hrs
                
    for m, d in ((1,31),(2,28),(3,31),(4,30),(5,31),(6,30),(7,31)):
        for _d in range(1, d+1):
            start_time = datetime(year=2023, month=m, day=_d).timestamp()
            _date = datetime(year=2023, month=m, day=_d).strftime(DEFAULT_DATE_FORMAT)
            hours_worked = 0
            hours_tobe_worked = random.randint(4, 8)
            
            while hours_worked < hours_tobe_worked:
                session_hrs = random.randint(0, 4)
                if session_hrs != 0:
                    create_work_session(_date, random.choice(activities), start_time, start_time+(session_hrs*3600))
                    start_time = start_time+(session_hrs*3600)
                    hours_worked += session_hrs

if __name__ == "__main__":
    
    print(DEFAULT_DB_FILE_PATH)
    init_database()
    generate_fake_worksessions()
