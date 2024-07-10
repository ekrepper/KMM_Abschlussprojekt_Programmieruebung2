import sqlite3
import pandas as pd
import streamlit as st

# Initialisierung des Session State
if 'show_user_form' not in st.session_state:
    st.session_state.show_user_form = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# User anlegen
def create_user():
    """
    Creates the 'user' table in the database if it doesn't exist.
    """
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
    """
    Inserts a new user into the 'user' table.
    
    Args:
        user_id (str): The user ID.
        vorname (str): The first name of the user.
        nachname (str): The last name of the user.
        geburtsdatum (str): The birth date of the user.
        max_hr (int): The maximum heart rate of the user.
    """
    user_id = geburtsdatum.strftime('%Y%m%d')
    conn = sqlite3.connect('fitfile_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO user (user_id, vorname, nachname, geburtsdatum, max_hr) VALUES (?, ?, ?, ?, ?)", (user_id, vorname, nachname, geburtsdatum, max_hr))
    conn.commit()
    conn.close()

def get_user():
    """
    Retrieves the list of users from the 'user' table.
    
    Returns:
        list: The list of users in the format "user_id - name".
    """
    conn = sqlite3.connect('fitfile_data.db')
    df = pd.read_sql_query("SELECT user_id, vorname || ' ' || nachname AS name FROM user", conn)
    conn.close()
    users = df.apply(lambda row: f"{row['user_id']} - {row['name']}", axis=1).tolist()
    if df.empty:
        st.sidebar.write("Keine Benutzer/innen vorhanden - legen Sie Athlet/innen an.")
    return users

def get_active_user_id():
    """
    Retrieves the active user ID from the 'active_User' table.
    
    Returns:
        str: The active user ID.
    """
    conn = sqlite3.connect('fitfile_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT active_User FROM active_User LIMIT 1")  # Annahme: es gibt immer nur einen aktiven Benutzer
    active_user_id = cursor.fetchone()
    conn.close()
    return active_user_id[0] if active_user_id else None

def delete_user(user_id):
    """
    Deletes a user from the 'user' table.
    
    Args:
        user_id (str): The user ID of the user to be deleted.
    """
    conn = sqlite3.connect('fitfile_data.db')
    c = conn.cursor()
    delete_sql = f"""
        DELETE FROM user WHERE user_id = '{user_id}'
    """
    delete_sql_1 = f"""
        DELETE FROM trainings WHERE user_id = '{user_id}'
    """
    try:
        c.execute(delete_sql)
        c.execute(delete_sql_1)
        conn.commit()
        st.write("Benutzer erfolgreich gelöscht.")
    except sqlite3.Error as e:
        st.write(f"Fehler beim Löschen des Benutzers: {e}")
    finally:
        conn.close()


# Trainingsdaten

def create_table():
    """
    Creates the 'trainings' table in the database if it doesn't exist.
    """
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
            time_zone_1 TIME,
            time_zone_2 TIME,
            time_zone_3 TIME,
            time_zone_4 TIME,
            time_zone_5 TIME,
            user_id TEXT,
            FOREIGN KEY (user_id) REFERENCES user(user_id)
        )
    ''')
    conn.commit()
    conn.close()


def get_training_data():
    """
    Retrieves the training data for the active user from the 'trainings' table.
    
    Returns:
        pandas.DataFrame: The training data.
    """
    conn = sqlite3.connect('fitfile_data.db')
    user_id = get_active_user_id()
    query = f"""
        SELECT activity_kw, activity_date, SUM(activity_total_distance) AS total_distance
        FROM trainings WHERE user_id = '{user_id}'
        GROUP BY activity_kw, activity_date
        ORDER BY activity_date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_training_data_by_week(week):
    """
    Retrieves the training data for a specific week for the active user from the 'trainings' table.
    
    Args:
        week (int): The week number.
    
    Returns:
        pandas.DataFrame: The training data for the specified week.
    """
    conn = sqlite3.connect('fitfile_data.db')
    user_id = get_active_user_id()
    query = f"""
        SELECT activity_date, activity_total_distance AS total_distance
        FROM trainings WHERE user_id = '{user_id}' AND activity_kw = {week}
        ORDER BY activity_date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_overview_data():
    """
    Retrieves the overview data for the active user from the 'trainings' table.
    
    Returns:
        pandas.DataFrame: The overview data.
    """
    conn = sqlite3.connect('fitfile_data.db')
    user_id = get_active_user_id()
    query = f"""
        SELECT
            activity_id, 
            activity_date, 
            activity_total_distance AS total_distance, 
            activity_duration AS total_duration, 
            activity_avg_hr AS avg_hr, 
            activity_avg_pace AS avg_pace,
            time_zone_1,
            time_zone_2,
            time_zone_3,
            time_zone_4,
            time_zone_5
        FROM 
            trainings WHERE user_id = '{user_id}'
        GROUP BY 
            activity_date, activity_duration
        ORDER BY 
            activity_date, activity_duration 
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_summary_data(start_date, end_date):
    """
    Retrieves the summary data for a specific date range for the active user from the 'trainings' table.
    
    Args:
        start_date (str): The start date of the date range.
        end_date (str): The end date of the date range.
    
    Returns:
        pandas.DataFrame: The summary data.
    """
    conn = sqlite3.connect('fitfile_data.db')
    user_id = get_active_user_id()
    query = f"""
        SELECT 
            SUM(activity_total_distance) AS total_distance,
            time(SUM(strftime('%s', activity_duration)), 'unixepoch') AS total_duration_formatted,
            AVG(activity_avg_hr) AS avg_hr
            
        FROM 
            trainings
        WHERE 
            activity_date BETWEEN '{start_date}' AND '{end_date}' AND user_id = '{user_id}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def delete_entry(delete_id):
    """
    Deletes an entry from the 'trainings' table.
    
    Args:
        delete_id (int): The ID of the entry to be deleted.
    """
    conn = sqlite3.connect('fitfile_data.db')
    c = conn.cursor()
    delete_sql = f"""
        DELETE FROM trainings WHERE activity_id = '{delete_id}'
    """
    try:
        c.execute(delete_sql)
        conn.commit()
        st.write("Eintrag erfolgreich gelöscht - Seite neu laden, dann wird Eintrag aus der Übersicht entfernt.")
    except sqlite3.Error as e:
        st.write(f"Fehler beim Löschen des Eintrags: {e}")
    finally:
        conn.close()



# Bestleistungen

def create_database():
    """
    Creates the 'bestleistungen' table in the database if it doesn't exist.
    """
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


def insert_bestleistung(strecke, zeit, datum):
    """
    Inserts a new bestleistung into the 'bestleistungen' table.
    
    Args:
        strecke (str): The distance of the bestleistung.
        zeit (str): The time of the bestleistung.
        datum (str): The date of the bestleistung.
    """
    conn = sqlite3.connect('bestleistungen.db')
    c = conn.cursor()
    c.execute("INSERT INTO bestleistungen (strecke, zeit, datum) VALUES (?, ?, ?)", (strecke, zeit, datum))
    conn.commit()
    conn.close()

def get_bestleistungen():
    """
    Retrieves the bestleistungen from the 'bestleistungen' table.
    
    Returns:
        pandas.DataFrame: The bestleistungen.
    """
    conn = sqlite3.connect('bestleistungen.db')
    df = pd.read_sql_query("SELECT * FROM bestleistungen", conn)
    conn.close()
    return df

if __name__ == "__main__":
    conn = sqlite3.connect('fitfile_data.db')
    c = conn.cursor()
    
    delete_sql = """
       Drop table trainings
    """
    try:
        c.execute(delete_sql)
        conn.commit()
        print("Eintrag erfolgreich gelöscht.")
    except sqlite3.Error as e:
        print(f"Fehler beim Löschen des Eintrags: {e}")
    finally:
        conn.close()