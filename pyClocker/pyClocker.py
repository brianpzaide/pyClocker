from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from . import SUCCESS, CREATE_SESSION_ERROR, STOP_SESSION_ERROR
from .database import DatabaseHandler, DailyWorkHours

from tabulate import tabulate

import pandas as pd

class PyClocker:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
    
    def start(self, activity) -> int:
        """Start a new session."""
        current_session = self._db_handler.get_current_work_session()
        # for the first time use
        if current_session is None:
            self._db_handler.create_work_session(activity)
            return SUCCESS

        if current_session.stop_time is None:
            return CREATE_SESSION_ERROR
        else:
            self._db_handler.create_work_session(activity)
            return SUCCESS
    
    def stop(self) -> int:
        """End current session."""
        current_session = self._db_handler.get_current_work_session()
        # for the first time use
        if current_session is None:
            return STOP_SESSION_ERROR

        if current_session.stop_time:
            return STOP_SESSION_ERROR
        else:
            self._db_handler.end_work_session(current_session.id)
            return SUCCESS
    
    def hours_put_in_today(self) -> str:
        """Get number of hours put in today."""
        worksessions_for_today = self._db_handler.get_time_spent_on_work_for_today()
        hours_per_activity = defaultdict(float)
        hours_spent_today = []

        for ws in worksessions_for_today:
            hours_per_activity[ws.activity] += (ws.stop_time - ws.start_time)/3600
        
        for activity, hrs in hours_per_activity.items():
            hours_spent_today.append([activity, '{0:.2f}'.format(hrs)])
        return tabulate(hours_spent_today, headers = ["activity", "time spent(hours)"])
        
    
    def hours_put_in_daily(self) -> Tuple[pd.DataFrame, List[str]]:
        """Get number of hours put in everyday."""
        df, activities = self._db_handler.get_daily_time_spent_on_work()
        new_df = df.pivot_table(index='date', columns='activity', values='hours', fill_value=0)
        new_df.reset_index(inplace=True)
        # print("original df")
        # print(df.head())
        # print("new df")
        # print(new_df.head())
        return new_df, activities