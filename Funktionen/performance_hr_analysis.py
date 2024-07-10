import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def get_heart_rate_zone(heart_rate, max_hr):
    """
    Determines the heart rate zone based on the given heart rate and maximum heart rate.

    Parameters:
    heart_rate (float): The heart rate value.
    max_hr (float): The maximum heart rate.

    Returns:
    str: The heart rate zone ('Zone1', 'Zone2', 'Zone3', 'Zone4', or 'Zone5').
    """
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

def analyze_heart_rate(df, max_hr):
    """
    Analyzes the heart rate data in the given DataFrame and calculates the time spent in each heart rate zone.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing heart rate data.
    max_hr (float): The maximum heart rate.

    Returns:
    pandas.Series: The time spent in each heart rate zone.
    """
    df['HeartRateZone'] = df['HeartRate'].apply(lambda x: get_heart_rate_zone(x, max_hr))
    time_in_zones = df.groupby('HeartRateZone')['Duration'].sum()
    time_in_zones = time_in_zones.apply(lambda x: '{:02}:{:02}'.format(int(x) // 60, int(x) % 60))
    return time_in_zones

def analyze_performance(df):
    """
    Analyzes the performance data in the given DataFrame and calculates the average performance in each heart rate zone.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing performance data.

    Returns:
    pandas.Series: The average performance in each heart rate zone.
    """
    avg_performance_in_zones = df.groupby('HeartRateZone')['PowerOriginal'].mean()
    avg_performance_in_zones = avg_performance_in_zones.round().astype(int)
    return avg_performance_in_zones

