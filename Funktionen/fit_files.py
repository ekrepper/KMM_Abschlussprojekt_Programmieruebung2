import fitparse
import numpy as np
import datetime as datetime
import streamlit as st

class FitFile:
    def __init__(self, fit_file, user_id=None):
        self.fit_file = fit_file
        self.dateref = datetime.datetime(1970, 1, 1)
        self.heartrate = np.array([])
        self.time = np.array([])
        self.distance = np.array([])
        self.avg_hr = None
        self.avg_speed = None
        self.total_distance = None
        self.total_timer_time = None
        self.timestamp = None
        self.user_id = user_id
        self.load_fit_file()

    def load_fit_file(self):
        try:
            fitfile = fitparse.FitFile(self.fit_file)
        except Exception as e:
            st.error(f"Error loading FIT file: {e}")
            return
        
        for record in fitfile.get_messages("record"):
            for data in record:
                if data.name == 'heart_rate':
                    self.heartrate = np.append(self.heartrate, data.value)
                elif data.name == 'timestamp':
                    self.time = np.append(self.time, (data.value - self.dateref).total_seconds())
                elif data.name == 'distance':
                    self.distance = np.append(self.distance, data.value)
        
        for session in fitfile.get_messages("session"):
            for data in session:
                if data.name == "avg_heart_rate":
                    self.avg_hr = data.value
                if data.name == "avg_speed":
                    self.avg_speed = data.value
                if data.name == "total_distance":
                    self.total_distance = data.value
                if data.name == "total_timer_time":
                    self.total_timer_time = data.value
                if data.name == "timestamp":
                    self.timestamp = data.value

    def get_total_distance(self):
        if self.total_distance is not None:
            total_distance_km = self.total_distance / 1000
            return total_distance_km
        else:
            return None
    
    def get_avg_hr(self):
        return self.avg_hr
    
    def get_avg_pace(self):
        if self.avg_speed is not None:
            pace = 60 / (self.avg_speed * 3.6)  # Umrechnen von m/s in km/h und dann in min/km
            minutes = int(pace)
            seconds = int((pace - minutes) * 60)
            return f"{minutes}:{seconds:02d}"
        else:
            return None
        
    def get_total_time(self):
        if self.total_timer_time is not None:
            hours = int(self.total_timer_time // 3600)
            minutes = int((self.total_timer_time % 3600) // 60)
            seconds = int(self.total_timer_time % 60)
            total_time = f"{hours:02}:{minutes:02}:{seconds:02}"
            return total_time
        else:
            return None
    
    def get_date(self):
        if self.timestamp is not None:
            date_str = self.timestamp.strftime('%Y-%m-%d')
            return date_str
        else:
            return None
    
    def get_calendar_week(self):
        if self.timestamp is not None:
            calendar_week = self.timestamp.isocalendar()[1]
            return calendar_week
        else:
            return None

    def get_insert_statement(self):
        """Erstellt eine SQL-Insert-Anweisung für die trainings-Tabelle basierend auf den gesammelten Daten"""
        if not all([self.timestamp, self.total_timer_time, self.total_distance]):
            st.error("Fehlende Daten für Insert-Anweisung.")
            return None
        
        insert_sql = f"""
            INSERT INTO 'trainings' (
                activity_date,
                activity_kw,
                activity_duration,
                activity_total_distance,
                activity_avg_pace,
                activity_avg_hr,
                user_id
            ) VALUES (
                '{self.get_date()}',
                {self.get_calendar_week()},
                '{self.get_total_time()}',
                {self.get_total_distance()},
                '{self.get_avg_pace()}',
                {self.get_avg_hr()},
                {self.user_id}
            );
        """
        return insert_sql
