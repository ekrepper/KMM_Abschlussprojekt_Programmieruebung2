import fitparse
import numpy as np
import datetime as datetime
import streamlit as st
import pandas as pd

class FitFile:
    def __init__(self, fit_file, user_id = None):
        self.fit_file = fitparse.FitFile(fit_file)
        self.dateref = datetime.datetime(1970, 1, 1)
        self.heartrate = self.get_heartrate()
        self.time = self.get_time()
        self.distance = self.get_distance()
        self.avg_hr = self.get_avg_hr()
        self.avg_speed = self.get_avg_speed()    
        self.total_distance = self.get_total_distance()
        self.total_timer_time = self.get_total_time()
        self.timestamp = self.get_timestamp()
        self.date = self.get_date()
        self.calendar_week = self.get_calendar_week()
        self.heartrate_zones = self.get_heartrate_zones(211)  # 220 - 30 = 190 (max. Herzfrequenz)
        self.time_zone_1 = self.get_time_in_zones(self.heartrate_zones["Zone 1"])
        self.time_zone_2 = self.get_time_in_zones(self.heartrate_zones["Zone 2"])
        self.time_zone_3 = self.get_time_in_zones(self.heartrate_zones["Zone 3"])
        self.time_zone_4 = self.get_time_in_zones(self.heartrate_zones["Zone 4"])
        self.time_zone_5 = self.get_time_in_zones(self.heartrate_zones["Zone 5"])
        self.user_id = user_id

    def get_heartrate(self):
        heartrate = np.array([])
        for record in self.fit_file.get_messages("record"):
            for data in record:
                if data.name == 'heart_rate':
                    heartrate = np.append(heartrate, data.value)
                else:
                     continue
        return heartrate
    
    def get_time(self):
        time = np.array([])
        for record in self.fit_file.get_messages("record"):
            for data in record:
                if data.name == 'timestamp':
                    time = np.append(time, (data.value - self.dateref).total_seconds())
                else:
                     continue
        return time
    
    def get_distance(self):
        distance = np.array([])
        for record in self.fit_file.get_messages("record"):
            for data in record:
                if data.name == 'distance':
                    distance = np.append(distance, data.value)
                else:
                     continue
        return distance
    
    def get_avg_hr(self):
        for session in self.fit_file.get_messages("session"):
            for data in session:
                if data.name == "avg_heart_rate":
                    avg_hr = data.value
                else:
                    continue
        return avg_hr

    def get_total_distance(self):
        for session in self.fit_file.get_messages("session"):
            for data in session:
                if data.name == "total_distance":
                    total_distance = data.value
                else:
                    continue
        return total_distance / 1000  # Umrechnen von m in km   
    
    def get_avg_speed(self):
        for session in self.fit_file.get_messages("session"):
            for data in session:
                if data.name == "avg_speed":
                    avg_speed = data.value
                else:
                    continue
        pace = 60 / (avg_speed * 3.6)  # Umrechnen von m/s in km/h und dann in min/km
        minutes = int(pace)
        seconds = int((pace - minutes) * 60)
        return f"{minutes}:{seconds:02d}"  
        
    def get_total_time(self):
        for session in self.fit_file.get_messages("session"):
            for data in session:
                if data.name == "total_timer_time":
                    total_timer_time = data.value
                else:
                    continue
        hours = int(total_timer_time // 3600)
        minutes = int((total_timer_time % 3600) // 60)
        seconds = int(total_timer_time % 60)
        total_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        return total_time
    
    def get_timestamp(self):
        for session in self.fit_file.get_messages("session"):
            for data in session:
                if data.name == "timestamp":
                    timestamp = data.value
                else:
                    continue
        return timestamp
    
    def get_date(self):
        date_str = self.timestamp.strftime('%Y-%m-%d')
        return date_str
  
    def get_calendar_week(self):
        calendar_week = self.timestamp.isocalendar()[1]
        return calendar_week

    def get_heartrate_zones(self, max_heartrate):
        zone_1 = np.where(self.heartrate < 0.6 * max_heartrate)
        zone_2 = np.where(np.logical_and(self.heartrate >= 0.6 * max_heartrate, self.heartrate < 0.7 * max_heartrate))
        zone_3 = np.where(np.logical_and(self.heartrate >= 0.7 * max_heartrate, self.heartrate < 0.8 * max_heartrate))  
        zone_4 = np.where(np.logical_and(self.heartrate >= 0.8 * max_heartrate, self.heartrate < 0.9 * max_heartrate))
        zone_5 = np.where(self.heartrate >= 0.9 * max_heartrate)
        data = {"Zone 1" : zone_1[0],
                "Zone 2" : zone_2[0],
                "Zone 3" : zone_3[0],
                "Zone 4" : zone_4[0],
                "Zone 5" : zone_5[0]}
        return data
    
    def get_time_in_zones(self, data):
        time_zone = np.size(data)
        minutes = int((time_zone % 3600) // 60)
        seconds = int(time_zone % 60)
        return f"{minutes:02}:{seconds:02}"

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
                '{self.date}',
                {self.calendar_week},
                '{self.total_timer_time}',
                {self.total_distance},
                '{self.avg_speed}',
                {self.avg_hr},
                {self.user_id}
            );
        """
        return insert_sql


if __name__ == "__main__":
    fit = FitFile("data/Fit_files/Running_2024-06-04T13_16_40-1.fit")
    print(fit.avg_hr)
    print(fit.avg_speed)   
    print(fit.total_distance)   