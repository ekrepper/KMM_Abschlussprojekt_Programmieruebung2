import fitparse
import numpy as np
import datetime as datetime
import streamlit as st

# Import necessary libraries

import fitparse  # Library for parsing FIT files
import numpy as np  # Library for numerical operations
import datetime as datetime  # Library for working with dates and times
import streamlit as st  # Library for building interactive web apps
import pandas as pd  # Library for data manipulation and analysis

class FitFile:
    """Represents a FIT file and provides methods to extract data from it."""

    def __init__(self, fit_file, user_id=None, m_heartrate = None):
        """
        Initialize the FitFile object with the provided FIT file and optional user ID.

        Parameters:
        - fit_file (str): The path to the FIT file.
        - user_id (str, optional): The ID of the user. Defaults to None.
        """
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
        self.sampling_rate = self.get_samling_rate()
        self.max_heartrate = m_heartrate
        self.heartrate_zones = self.get_heartrate_zones(self.max_heartrate)
        self.time_zone_1 = self.get_time_in_zones(self.heartrate_zones["Zone 1"])
        self.time_zone_2 = self.get_time_in_zones(self.heartrate_zones["Zone 2"])
        self.time_zone_3 = self.get_time_in_zones(self.heartrate_zones["Zone 3"])
        self.time_zone_4 = self.get_time_in_zones(self.heartrate_zones["Zone 4"])
        self.time_zone_5 = self.get_time_in_zones(self.heartrate_zones["Zone 5"])
        self.user_id = user_id

    def get_heartrate(self):
        """
        Retrieve the heart rate data from the FIT file.

        Returns:
        - heartrate (numpy.ndarray): An array of heart rate values.
        """
        heartrate = np.array([])
        for record in self.fit_file.get_messages("record"):
            for data in record:
                if data.name == 'heart_rate':
                    heartrate = np.append(heartrate, data.value)
                else:
                    continue
        return heartrate
    
    def get_time(self):
        """
        Retrieve the time data from the FIT file.

        Returns:
        - time (numpy.ndarray): An array of time values.
        """
        time = np.array([])
        for record in self.fit_file.get_messages("record"):
            for data in record:
                if data.name == 'timestamp':
                    time = np.append(time, (data.value - self.dateref).total_seconds())
                else:
                    continue
        return time
    
    def get_distance(self):
        """
        Retrieve the distance data from the FIT file.

        Returns:
        - distance (numpy.ndarray): An array of distance values.
        """
        distance = np.array([])
        for record in self.fit_file.get_messages("record"):
            for data in record:
                if data.name == 'distance':
                    distance = np.append(distance, data.value)
                else:
                    continue
        return distance
    
    def get_avg_hr(self):
        """
        Calculate the average heart rate from the FIT file.

        Returns:
        - avg_hr (float): The average heart rate.
        """
        for session in self.fit_file.get_messages("session"):
            for data in session:
                if data.name == "avg_heart_rate":
                    avg_hr = data.value
                else:
                    continue
        return avg_hr

    def get_total_distance(self):
        """
        Calculate the total distance from the FIT file.

        Returns:
        - total_distance (float): The total distance in kilometers.
        """
        for session in self.fit_file.get_messages("session"):
            for data in session:
                if data.name == "total_distance":
                    total_distance = data.value
                else:
                    continue
        return total_distance / 1000  # Convert from meters to kilometers
    
    def get_avg_speed(self):
        """
        Calculate the average speed and pace from the FIT file.

        Returns:
        - avg_speed (str): The average speed in the format "mm:ss" (minutes:seconds).
        """
        for session in self.fit_file.get_messages("session"):
            for data in session:
                if data.name == "avg_speed":
                    avg_speed = data.value
                else:
                    continue
        pace = 60 / (avg_speed * 3.6)  # Convert from m/s to km/h and then to min/km
        minutes = int(pace)
        seconds = int((pace - minutes) * 60)
        return f"{minutes}:{seconds:02d}"  
        
    def get_total_time(self):
        """
        Calculate the total time from the FIT file.

        Returns:
        - total_time (str): The total time in the format "hh:mm:ss" (hours:minutes:seconds).
        """
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
        """
        Retrieve the timestamp from the FIT file.

        Returns:
        - timestamp (datetime.datetime): The timestamp.
        """
        for session in self.fit_file.get_messages("session"):
            for data in session:
                if data.name == "timestamp":
                    timestamp = data.value
                else:
                    continue
        return timestamp
    
    def get_date(self):
        """
        Format the timestamp as a date string.

        Returns:
        - date_str (str): The date string in the format "YYYY-MM-DD".
        """
        date_str = self.timestamp.strftime('%Y-%m-%d')
        return date_str
  
    def get_calendar_week(self):
        """
        Calculate the calendar week from the timestamp.

        Returns:
        - calendar_week (int): The calendar week.
        """
        calendar_week = self.timestamp.isocalendar()[1]
        return calendar_week
    
    def get_samling_rate(self):
        """
        Calculate the sampling rate of the heart rate data.

        Returns:
        - sampling_rate (float): The sampling rate in Hz.
        """
        sampling_rate = (self.time[-1] - self.time[0]) / len(self.time)
        return sampling_rate

    def get_heartrate_zones(self, max_heartrate):
        """
        Calculate the heart rate zones based on the maximum heart rate.

        Parameters:
        - max_heartrate (int): The maximum heart rate.

        Returns:
        - data (dict): A dictionary containing the heart rate zones.
        """
        zone_1 = np.where(self.heartrate < 0.71 * max_heartrate)
        zone_2 = np.where(np.logical_and(self.heartrate >= 0.71 * max_heartrate, self.heartrate < 0.76 * max_heartrate))
        zone_3 = np.where(np.logical_and(self.heartrate >= 0.76 * max_heartrate, self.heartrate < 0.81 * max_heartrate))  
        zone_4 = np.where(np.logical_and(self.heartrate >= 0.81 * max_heartrate, self.heartrate < 0.87 * max_heartrate))
        zone_5 = np.where(self.heartrate >= 0.87 * max_heartrate)
        data = {"Zone 1" : zone_1[0],
                "Zone 2" : zone_2[0],
                "Zone 3" : zone_3[0],
                "Zone 4" : zone_4[0],
                "Zone 5" : zone_5[0]}
        return data
    
    def get_time_in_zones(self, zone_indices):
        """
        Calculate the time spent in a heart rate zone.

        Parameters:
        - zone_indices (numpy.ndarray): An array of indices representing the heart rate zone.

        Returns:
        - time_str (str): The time spent in the heart rate zone in the format "hh:mm:ss" (hours:minutes:seconds).
        """
        if len(zone_indices) == 0:
            return "00:00:00"
        
        total_time_in_seconds = len(zone_indices) * self.sampling_rate  # Calculate the total time in seconds
        
        hours = int(total_time_in_seconds // 3600)
        minutes = int((total_time_in_seconds % 3600) // 60)
        seconds = int(total_time_in_seconds % 60)
        
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        return time_str

    def get_insert_statement(self):
        """
        Create an SQL INSERT statement for the 'trainings' table based on the collected data.

        Returns:
        - insert_sql (str): The SQL INSERT statement.
        """
        if not all([self.timestamp, self.total_timer_time, self.total_distance]):
            st.error("Missing data for INSERT statement.")
            return None
            
        insert_sql = f"""
            INSERT INTO 'trainings' (
                activity_date,
                activity_kw,
                activity_duration,
                activity_total_distance,
                activity_avg_pace,
                activity_avg_hr,
                time_zone_1,
                time_zone_2,
                time_zone_3,
                time_zone_4,
                time_zone_5,
                user_id
            ) VALUES (
                '{self.date}',
                '{self.calendar_week}',
                '{self.total_timer_time}',
                '{self.total_distance}',
                '{self.avg_speed}',
                '{self.avg_hr}',
                '{self.time_zone_1}',
                '{self.time_zone_2}',
                '{self.time_zone_3}',
                '{self.time_zone_4}',
                '{self.time_zone_5}',
                '{self.user_id}'
            );
        """
        return insert_sql
    


if __name__ == "__main__":
    data = FitFile("data/Fit_files/Running_2024-07-09T09_37_19.fit", "1", 211)
    print(data.time_zone_1)
    print(data.time_zone_2)
    print(data.time_zone_3)
    print(data.time_zone_4)
    print(data.time_zone_5)

