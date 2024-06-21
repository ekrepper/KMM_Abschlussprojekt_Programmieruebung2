import fitparse
import numpy as np
import datetime as datetime
from collections import defaultdict

class FitFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.dateref = datetime.datetime(1970, 1, 1)
        self.heartrate = np.array([])
        self.time = np.array([])
        self.distance = np.array([])
        self.speed = np.array([])
        self.avg_hr = None
        self.avg_speed = None
        self.total_distance = None
        self.total_timer_time = None
        self.timestamp = None
        self.load_fit_file()

    def load_fit_file(self):
        try:
            fitfile = fitparse.FitFile(self.filepath)
        except Exception as e:
            print(f"Error loading FIT file: {e}")
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

    def get_heartrate(self):
        return self.heartrate

    def get_time(self):
        return self.time

    def get_distance(self):
        return self.distance
    
    def get_total_distance(self):
        if self.total_distance is not None:
            total_distance_km = self.total_distance / 1000
            return total_distance_km
        else:
            return "No total distance data available"
    
    def get_avg_hr(self):
        return self.avg_hr
    
    def get_avg_pace(self):
        if self.avg_speed is not None:
            pace = 60 / (self.avg_speed * 3.6)  # Umrechnen von m/s in km/h und dann in min/km
            minutes = int(pace)
            seconds = int((pace - minutes) * 60)
            return f"{minutes}:{seconds:02d}"
        else:
            return "No avg pace data available"
        
    def get_total_time(self):
        if self.total_timer_time is not None:
            hours = int(self.total_timer_time // 3600)
            minutes = int((self.total_timer_time % 3600) // 60)
            seconds = int(self.total_timer_time % 60)
            total_time = f"{hours:02}:{minutes:02}:{seconds:02}"
            return total_time
        else:
            return "No total elapsed time data available"
    
    def get_date(self):
        if self.timestamp is not None:
            date_str = self.timestamp.strftime('%d.%m.%y')
            return date_str
        else:
            return "No timestamp data available"
    
    def get_calendar_week(self):
        if self.timestamp is not None:
            calendar_week = self.timestamp.isocalendar()[1]
            return calendar_week
        else:
            return "No timestamp data available"

    '''def print_data(self):
        total_distance_km = self.get_total_distance()
        print("Total Distance (km):", total_distance_km)
        print("Avg Heart Rate (bpm):", self.avg_hr if self.avg_hr is not None else "No avg heart rate data available")
        avg_pace = self.get_avg_pace()
        print("Avg Pace (min/km):", avg_pace)
        total_time = self.get_total_time()
        print("Total Time (hh:mm:ss):", total_time)
        date_str = self.get_date()
        print("Date:", date_str)
        calendar_week = self.get_calendar_week()
        print("Calendar Week:", calendar_week)'''

# Verwendung der Klasse
filepath = "data/activities/Running_2024-06-04T13_16_40.fit"
fit_parser = FitFile(filepath)
#fit_parser.print_data()
