import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Funktion zur Zoneneinteilung basierend auf der Herzfrequenz und der maximalen Herzfrequenz
def get_heart_rate_zone(heart_rate, max_hr):
    if heart_rate < 0.6 * max_hr:
        return 'Zone1'
    elif heart_rate < 0.7 * max_hr:
        return 'Zone2'
    elif heart_rate < 0.8 * max_hr:
        return 'Zone3'
    elif heart_rate < 0.9 * max_hr:
        return 'Zone4'
    else:
        return 'Zone5'

# Funktion zur Analyse der Herzfrequenz
def analyze_heart_rate(df, max_hr):
    df['HeartRateZone'] = df['HeartRate'].apply(lambda x: get_heart_rate_zone(x, max_hr))
    time_in_zones = df.groupby('HeartRateZone')['Duration'].sum()
    time_in_zones = time_in_zones.apply(lambda x: '{:02}:{:02}'.format(int(x) // 60, int(x) % 60))
    return time_in_zones

# Funktion zur Analyse der Leistung
def analyze_performance(df):
    avg_performance_in_zones = df.groupby('HeartRateZone')['PowerOriginal'].mean()
    avg_performance_in_zones = avg_performance_in_zones.round().astype(int)
    return avg_performance_in_zones

