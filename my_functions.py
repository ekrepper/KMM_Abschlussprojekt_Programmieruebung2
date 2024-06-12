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