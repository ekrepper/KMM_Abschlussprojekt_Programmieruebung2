import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def activity_read_csv():
    """
    Reads the activity data from a CSV file.

    Returns:
        DataFrame: The activity data as a pandas DataFrame.
    """
    df = pd.read_csv("data/activities/activity.csv")
    return df


def calc_powercurve(df):
    """
    Calculates the power curve.

    Args:
        df (DataFrame): The input DataFrame containing the power data.

    Returns:
        DataFrame: The power curve as a pandas DataFrame.
    """
    df_clean = df.dropna(subset="PowerOriginal")
    array_best_effort = []
    array_time_window = []
    for window in range(1201):
        value = best_effort(df_clean, window)
        array_best_effort.append(value)
        array_time_window.append(window)
    powercurve_df = pd.DataFrame({"Power": array_best_effort, "Time_Window": array_time_window})
    desired_times = [1, 30, 60, 100, 300, 600, 1200]
    return powercurve_df


def best_effort(df, window):
    """
    Calculates the best effort power within a given time window.

    Args:
        df (DataFrame): The input DataFrame containing the power data.
        window (int): The size of the time window.

    Returns:
        float: The maximum power value within the time window.
    """
    value = df["PowerOriginal"].rolling(window).mean()
    return value.max()