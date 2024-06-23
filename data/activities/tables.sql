-- Tabelle für Aktivitäten 
CREATE TABLE trainings (
    activity_id INTEGER PRIMARY KEY,
    activity_date DATE,
    activity_kw INTEGER,
    activity_duration TIME,
    activity_total_distance FLOAT,
    activity_avg_pace TIME,
    activity_avg_hr INTEGER
)

