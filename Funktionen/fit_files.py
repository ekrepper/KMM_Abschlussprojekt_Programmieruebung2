import fitparse
import numpy as np
import datetime as datetime

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
        self.load_fit_file()

    def load_fit_file(self):
        fitfile = fitparse.FitFile(self.filepath)
        
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

    def get_heartrate(self):
        return self.heartrate

    def get_time(self):
        return self.time

    def get_distance(self):
        return self.distance
    
    def get_total_distance(self):
        total_distance_km = self.total_distance
        return self.total_distance_km
    
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
    
    def print_data(self):
        print("Heart Rate:", self.heartrate)
        print("Time:", self.time)
        print("Distance:", self.distance)
        print("Total Distance:", self.total_distance if self.total_distance is not None else "No total distance data available")
        print("Avg Heart Rate:", self.avg_hr if self.avg_hr is not None else "No avg heart rate data available")
        avg_pace = self.get_avg_pace()
        print("Avg Pace (min/km):", avg_pace if avg_pace is not None else "No avg pace data available")

# Verwendung der Klasse
filepath = "data/activities/Running_2024-06-04T13_16_40.fit"
parser = FitFile(filepath)
parser.print_data()
