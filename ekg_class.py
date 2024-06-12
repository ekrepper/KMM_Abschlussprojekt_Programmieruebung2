import json
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st
import plotly.graph_objects as go

class EKGdata:
    # Constructor to initialize the class with the data
    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV', 'Zeit in ms'])
        self.df_plot = self.df.head(10000)  # Limit to the first 10,000 data points
        self.peaks = self.find_peaks(self.df["Messwerte in mV"].copy(), 340)
        self.peaks_plot = self.find_peaks(self.df_plot["Messwerte in mV"].copy(), 340)   
        self.heartrate = self.calc_heartrate()
        self.max_heartrate = self.calc_max_heartrate()
        self.heartrate_time = self.calc_heartrate_time()
        self.duration = self.df["Zeit in ms"][len(self.df["Zeit in ms"]) - 1] / 1000


    def make_plot(self):
        # Create a line plot of the first 10,000 values with time on the x-axis
        fig = px.line(self.df_plot, x="Zeit in ms", y="Messwerte in mV", title="EKG Plot")
        fig2 = px.line(self.heartrate_time, x="Time in s", y="Heartrate", title="Herzfrequenz über die Zeit")
        

        # Add peaks to the plot
        peaks_x = self.df_plot["Zeit in ms"][self.peaks_plot]
        peaks_y = self.df_plot["Messwerte in mV"][self.peaks_plot]
        fig.add_trace(go.Scatter(x=peaks_x, y=peaks_y, mode='markers+text', name='Peaks', text=["R"]*len(peaks_x),
                                 textposition="top center", marker=dict(color='red', size=10)))

        # Display the plot in Streamlit
        st.plotly_chart(fig)
        st.plotly_chart(fig2)

    @staticmethod
    def load_by_id(id):
        with open("data/person_db.json") as file:
            person_data = json.load(file)
            for person in person_data:
                for ekg_test in person["ekg_tests"]:
                    if ekg_test["id"] == id:
                        return EKGdata(ekg_test)
        return None

    def find_peaks(self, series, threshold, respacing_factor=5):
        """
        A function to find the peaks in a series
        Args:
            - series (pd.Series): The series to find the peaks in
            - threshold (float): The threshold for the peaks
            - respacing_factor (int): The factor to respace the series
        Returns:
            - peaks (list): A list of the indices of the peaks
        """
        # Respace the series
        series = series.iloc[::respacing_factor]

        # Filter the series
        series = series[series>threshold]


        peaks = []
        last = 0
        current = 0
        next = 0

        for index, row in series.items():
            last = current
            current = next
            next = row

            if last < current and current > next and current > threshold:
                peaks.append(index-respacing_factor)

        return peaks


    
    def calc_heartrate(self):
        timehr = np.array(self.df["Zeit in ms"][self.peaks])
        
        if len(timehr) < 2:
            raise ValueError("Nicht genügend Datenpunkte zur Berechnung der Herzfrequenz.")
        
        t_puls = np.diff(timehr)
        
        # Entferne negative oder unrealistische Intervalle
        t_puls = t_puls[t_puls > 0]
        
        if len(t_puls) < 2:
            raise ValueError("Nicht genügend valide Intervall zur Berechnung der Herzfrequenz.")
        
        # Optional: Mittlere 80% der Daten zur Berechnung verwenden
        trimmed_t_puls = t_puls[int(len(t_puls) * 0.1) : int(len(t_puls) * 0.9)]
        
        heartrate = (1 / np.mean(trimmed_t_puls)) * 60 * 1000
        
        return heartrate


    def calc_max_heartrate(self):
        if len(self.peaks) < 2:
            return None  # Not enough data to calculate heart rate
        
        timehr = np.array(self.df["Zeit in ms"][self.peaks])
        t_puls = np.diff(timehr)
        
        # Ensure all intervals are positive
        t_puls = t_puls[t_puls > 0]
        
        if len(t_puls) == 0:
            return None  # No valid intervals
        
        # Find the minimum interval to calculate the maximum heart rate
        min_interval = np.min(t_puls)
        max_heartrate = (1 / min_interval) * 60 * 1000  # Convert ms to minutes
        return max_heartrate
    
    def calc_heartrate_time(self):
        if len(self.peaks) < 2:
            return None  # Not enough data to calculate heart rate
        
        timehr = np.array(self.df["Zeit in ms"][self.peaks])
        t_puls = np.diff(timehr)
        
        # Ensure all intervals are positive
        t_puls = t_puls[t_puls > 0]

        if len(t_puls) == 0:
            return None  # No valid intervals
        
        heartrate = (1 / t_puls) * 60 * 1000
        
        #Speichern der Daten in ei  DataFrame
        data = {"Heartrate" : heartrate,
                "Time in s" : timehr[:len(heartrate)] / 1000}
        heartrate = pd.DataFrame(data)
        
        return heartrate

    def calc_hfr(self):
        if len(self.peaks) < 2:
            return None  # Not enough data to calculate heart rate
        
        timehr = np.array(self.df["Zeit in ms"][self.peaks])
        t_puls = np.diff(timehr)
        
        # Ensure all intervals are positive
        t_puls = t_puls[t_puls > 0]

        if len(t_puls) == 0:
            return None  # No valid intervals
        
        hvr = (1 / np.std(t_puls)) * 60000

        return hvr

                
if __name__ == "__main__":
    ekg_1 = EKGdata.load_by_id(2)
