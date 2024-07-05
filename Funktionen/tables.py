import sqlite3
import fitparse as ff  # oder der passende Fitfile Parser
import pandas as pd
import streamlit as st

# Initialisierung des Session State
if 'show_user_form' not in st.session_state:
    st.session_state.show_user_form = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

#User anlegen 

def create_user():
    conn = sqlite3.connect('fitfile_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            vorname TEXT,
            nachname TEXT,
            geburtsdatum DATE,
            max_hr INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(user_id, vorname, nachname, geburtsdatum, max_hr):
    user_id = geburtsdatum.strftime('%Y%m%d')
    conn = sqlite3.connect('fitfile_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO user (user_id, vorname, nachname, geburtsdatum, max_hr) VALUES (?, ?, ?, ?, ?)", (user_id, vorname, nachname, geburtsdatum, max_hr))
    conn.commit()
    conn.close()

def get_user():
    conn = sqlite3.connect('fitfile_data.db')
    df = pd.read_sql_query("SELECT user_id, vorname || ' ' || nachname AS name FROM user", conn)
    conn.close()
    users = df.apply(lambda row: f"{row['user_id']} - {row['name']}", axis=1).tolist()
    users.append("Neue/n Athlet/in anlegen")
    return users

def get_active_user_id():
    conn = sqlite3.connect('fitfile_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT active_User FROM active_User LIMIT 1")  # Annahme: es gibt immer nur einen aktiven Benutzer
    active_user_id = cursor.fetchone()
    conn.close()
    return active_user_id[0] if active_user_id else None


#Trainingsdaten

def create_table():
    conn = sqlite3.connect('fitfile_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trainings (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_date DATE,
            activity_kw INTEGER,
            activity_duration TIME,
            activity_total_distance FLOAT,
            activity_avg_pace TIME,
            activity_avg_hr INTEGER,
            user_id TEXT,
            FOREIGN KEY (user_id) REFERENCES user(user_id)
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(uploaded_file, user_id):
    conn = sqlite3.connect('fitfile_data.db')
    c = conn.cursor()
    fit_parser = ff.FitFile(uploaded_file)
    """
    for record in fit_parser.get_messages('record'):
        activity_date = record.get_value('timestamp')
        activity_duration = record.get_value('timer_time')
        activity_total_distance = record.get_value('distance')
        activity_avg_pace = record.get_value('enhanced_avg_speed')
        activity_avg_hr = record.get_value('avg_heart_rate')
    """
    activity_date = fit_parser.date
    activity_duration = fit_parser.total_timer_time
    activity_total_distance = fit_parser.total_distance
    activity_avg_pace = fit_parser.avg_speed
    activity_avg_hr = fit_parser.avg_heart_rate
    
    # Einfügeabfrage mit Überprüfung auf Duplikate
    insert_sql = """
        INSERT OR IGNORE INTO trainings (
            activity_date, activity_kw, activity_duration, activity_total_distance, activity_avg_pace, activity_avg_hr, user_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    try:
        c.execute(insert_sql, (activity_date, activity_date.isocalendar()[1], activity_duration, activity_total_distance, activity_avg_pace, activity_avg_hr, user_id))
    except sqlite3.Error as e:
        print(f"Fehler beim Einfügen der Daten in die Datenbank: {e}")
    
    conn.commit()
    conn.close()

def get_training_data():
    conn = sqlite3.connect('fitfile_data.db')
    user_id = get_active_user_id()
    # st.text(user_id)
    query = f"""
        SELECT activity_kw, activity_date, SUM(activity_total_distance) AS total_distance
        FROM trainings WHERE user_id = '{user_id}'
        GROUP BY activity_kw, activity_date
        ORDER BY activity_date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    # st.text(df)
    return df

def get_training_data_by_week(week):
    conn = sqlite3.connect('fitfile_data.db')
    query = f"""
        SELECT activity_date, activity_total_distance AS total_distance
        FROM trainings
        WHERE activity_kw = {week}
        ORDER BY activity_date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_overview_data():
    conn = sqlite3.connect('fitfile_data.db')
    query = """
        SELECT 
            activity_date, 
            activity_total_distance AS total_distance, 
            activity_duration AS total_duration, 
            activity_avg_hr AS avg_hr, 
            activity_avg_pace AS avg_pace
        FROM 
            trainings
        GROUP BY 
            activity_date, activity_duration
        ORDER BY 
            activity_date, activity_duration 
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_summary_data(start_date, end_date):
    conn = sqlite3.connect('fitfile_data.db')
    query = f"""
        SELECT 
            SUM(activity_total_distance) AS total_distance,
            time(SUM(strftime('%s', activity_duration)), 'unixepoch') AS total_duration_formatted,
            time(AVG(activity_avg_pace)) AS avg_pace,
            AVG(activity_avg_hr) AS avg_hr
        FROM 
            trainings
        WHERE 
            activity_date BETWEEN '{start_date}' AND '{end_date}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def delete_entry(activity_id):
    conn = sqlite3.connect('fitfile_data.db')
    c = conn.cursor()
    
    delete_sql = """
        DELETE FROM trainings
        WHERE activity_id = ?
    """
    try:
        c.execute(delete_sql, (activity_id,))
        conn.commit()
        print("Eintrag erfolgreich gelöscht.")
    except sqlite3.Error as e:
        print(f"Fehler beim Löschen des Eintrags: {e}")
    finally:
        conn.close()



#Bestleistungen

def create_database():
    conn = sqlite3.connect('bestleistungen.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bestleistungen (
            id INTEGER PRIMARY KEY,
            strecke TEXT,
            zeit TEXT,
            datum DATE
        )
    ''')
    conn.commit()
    conn.close()

create_database()


# Funktion zum Einfügen der Bestleistung in die Datenbank
def insert_bestleistung(strecke, zeit, datum):
    conn = sqlite3.connect('bestleistungen.db')
    c = conn.cursor()
    c.execute("INSERT INTO bestleistungen (strecke, zeit, datum) VALUES (?, ?, ?)", (strecke, zeit, datum))
    conn.commit()
    conn.close()

# Funktion zum Abrufen der Bestleistungen aus der Datenbank
def get_bestleistungen():
    conn = sqlite3.connect('bestleistungen.db')
    df = pd.read_sql_query("SELECT * FROM bestleistungen", conn)
    conn.close()
    return df
