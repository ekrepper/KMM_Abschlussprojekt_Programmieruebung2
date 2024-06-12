import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Funktion zum einlesen der Activity Daten
def activity_read_csv():
    df = pd.read_csv("data/activities/activity.csv")
    return df


#berechnet die Powercurve
def calc_powercurve(df):
    df_clean = df.dropna(subset = "PowerOriginal")
    array_best_effort = []
    array_time_window = []
    for window in range(1201):
        value = best_effort(df_clean, window)
        array_best_effort.append(value)
        array_time_window.append(window)
    powercurve_df = pd.DataFrame({"Power" : array_best_effort, "Time_Window" : array_time_window})
    desired_times = [1, 30, 60, 100, 300, 600, 1200]
    return powercurve_df
        
def best_effort(df, window):
    value = df["PowerOriginal"].rolling(window).mean()
    return value.max()