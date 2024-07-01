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
        self.t_puls = self.calc_tpuls()   
        self.heartrate = self.calc_heartrate()
        self.max_heartrate = self.calc_max_heartrate()
        self.heartrate_time = self.calc_heartrate_time()
        self.duration = self.calculate_duration()
        
    def calculate_duration(self):
        # Calculate the duration in seconds by subtracting the first timestamp from the last
        duration_in_ms = self.df["Zeit in ms"].iloc[-1] - self.df["Zeit in ms"].iloc[0]
        return duration_in_ms / 1000  # Convert milliseconds to seconds

    def make_plot(self, start_time=None, end_time=None):
        if start_time is not None and end_time is not None:
            mask = (self.df["Zeit in ms"] >= start_time * 1000) & (self.df["Zeit in ms"] <= end_time * 1000)
            df_filtered = self.df[mask].reset_index(drop=True)
            peaks_filtered = self.find_peaks(df_filtered["Messwerte in mV"].copy(), 340)
            heartrate_time_filtered = self.calc_heartrate_time_filtered(df_filtered)
        else:
            df_filtered = self.df_plot
            peaks_filtered = self.peaks_plot
            heartrate_time_filtered = self.heartrate_time

        df_filtered["Zeit in s"] = df_filtered["Zeit in ms"] / 1000

        fig = px.line(df_filtered, x="Zeit in s", y="Messwerte in mV", title="EKG Plot")
        fig2 = px.line(heartrate_time_filtered, x="Time in s", y="Heartrate", title="Herzfrequenz über die Zeit")

        fig2.update_layout(xaxis_title="Zeit in s", yaxis_title="Herzfrequenz")
        
        if len(peaks_filtered) > 0:
            peaks_x = df_filtered["Zeit in s"].iloc[peaks_filtered]
            peaks_y = df_filtered["Messwerte in mV"].iloc[peaks_filtered]
            fig.add_trace(go.Scatter(x=peaks_x, y=peaks_y, mode='markers+text', name='Peaks', text=["R"]*len(peaks_x),
                                     textposition="top center", marker=dict(color='red', size=10)))

        st.plotly_chart(fig)
        st.plotly_chart(fig2)

    def calc_heartrate_time_filtered(self, df_filtered):
        peaks_filtered = self.find_peaks(df_filtered["Messwerte in mV"].copy(), 340)
        if len(peaks_filtered) > 1:
            t_puls_filtered = np.diff(df_filtered["Zeit in ms"].iloc[peaks_filtered])
            heartrate_filtered = (1 / t_puls_filtered) * 60 * 1000
            timehr_filtered = df_filtered["Zeit in ms"].iloc[peaks_filtered[:-1]]
            data_filtered = {"Heartrate": heartrate_filtered, "Time in s": timehr_filtered / 1000}
            heartrate_time_filtered = pd.DataFrame(data_filtered)
        else:
            heartrate_time_filtered = pd.DataFrame({"Heartrate": [], "Time in s": []})

        return heartrate_time_filtered
    
        
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

    def calc_tpuls(self):
        timehr = np.array(self.df["Zeit in ms"][self.peaks])
        
        if len(timehr) < 2:
            raise ValueError("Nicht genügend Datenpunkte zur Berechnung der Herzfrequenz.")
        
        t_puls = np.diff(timehr)
        
        # Entferne negative oder unrealistische Intervalle
        t_puls = t_puls[t_puls > 0]
        
        if len(t_puls) < 2:
            raise ValueError("Nicht genügend valide Intervall zur Berechnung der Herzfrequenz.")
        
        return t_puls
    
    def calc_heartrate(self):
        
        # Optional: Mittlere 80% der Daten zur Berechnung verwenden
        trimmed_t_puls = self.t_puls[int(len(self.t_puls) * 0.1) : int(len(self.t_puls) * 0.9)]
        
        heartrate = (1 / np.mean(trimmed_t_puls)) * 60 * 1000
        
        return heartrate


    def calc_max_heartrate(self):
        
        # Find the minimum interval to calculate the maximum heart rate
        min_interval = np.min(self.t_puls)
        max_heartrate = (1 / min_interval) * 60 * 1000  # Convert ms to minutes
        return max_heartrate
    
    def calc_heartrate_time(self):
        
        heartrate = (1 / self.t_puls) * 60 * 1000
        timehr = np.array(self.df["Zeit in ms"][self.peaks])
        
        #Speichern der Daten in ei  DataFrame
        data = {"Heartrate" : heartrate,
                "Time in s" : timehr[:len(heartrate)] / 1000}
        heartrate = pd.DataFrame(data)
        
        return heartrate

    def calc_hfr(self):

        hvr = (1 / np.std(self.t_puls)) * 60000

        return hvr

                
if __name__ == "__main__":
    ekg_1 = EKGdata.load_by_id(2)
