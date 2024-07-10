import streamlit as st
from PIL import Image
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import sys
import inspect
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
import sqlite3
from sqlite3 import Error
import time
import random

#from A_my_streamlit import read_data as rd
from Funktionen import performance_hr_analysis as pha 
from Funktionen import calc_powercurve as cp
from Funktionen import person_class as pc
from Funktionen import ekg_class as ekg
from Funktionen import fit_files as ff
from Funktionen import tables as tb
from Funktionen import export as exp

st.set_page_config(layout="centered", page_title="Sports & Health Database", page_icon="🏃‍♀️")
st.sidebar.title("🌐Navigation")
option = st.sidebar.selectbox("Select a page:", ["🏠Home", "🏥Patientendatenbank", "🏃Trainingsübersicht"])


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

# Eine Überschrift der ersten Ebene
if option == "🏠Home":
    st.title = "🏠Home"
 

    # Set page configuration
    
    page_title="Sports & Health Database",
    page_icon="⚕️",
    layout="centered",
    initial_sidebar_state="collapsed"


    # Add custom CSS for animations
    st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');

    .header {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin-top: 50px;
        color: #878787;
        animation: fadeInDown 2s;
    }

    .subheader {
        font-size: 1.5em;
        text-align: center;
        margin-top: 20px;
        color: #666;
        animation: fadeInUp 2s;
    }

    .bounce-button {
        display: block;
        margin: 30px auto;
        padding: 10px 20px;
        font-size: 1.2em;
        font-weight: bold;
        color: #fff;
        background-color: #4CAF50;
        border: none;
        border-radius: 5px;
        animation: bounce 2s infinite;
        cursor: pointer;
    }

    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-30px);
        }
        60% {
            transform: translateY(-15px);
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<div class="header animate__animated animate__fadeInDown">HEALTHCOACH</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader animate__animated animate__fadeInUp">Patienten- und Trainingsdaten im Überblick</div>', unsafe_allow_html=True)

# Bild laden
    image = Image.open("data/screenshots/HEALTHCOACH.png")

# HTML für zentrierte Anzeige
    st.markdown(
        f"""
        <style>
        .centered {{
            display: block;
            margin-left: auto;
            margin-right: auto;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Bild in der Mitte anzeigen
    st.image(image, caption="", use_column_width=True)

# oder alternativ mit HTML, um das Bild zu zentrieren:
    st.markdown(f'<div style="text-align:center"><img src="data:image/png;base64,{image}" alt="HEALTHCOACH Logo" class="centered"></div>', unsafe_allow_html=True)

    # Animated button
    #st.markdown('<button class="bounce-button">Get Started</button>', unsafe_allow_html=True)

    # Adding some interactivity
    # if st.button('Get Started'):
    #     # Add a progress bar
    #     st.write("Your progress is our progress")
    #     progress_bar = st.progress(0)

    #     for percent_complete in range(100):
    #         time.sleep(0.1)  # Simulate a long computation
    #         progress_bar.progress(percent_complete + 1)
        
    # Adding a delay to simulate loading
       #time.sleep(2)
    # Display the prompt after loading
        #st.write("Du hast geklickt, gewartet und... nichts ist passiert! Eine App allein wird keine Wunder vollbringen - für deine Fitness bist du selbst verantwortlich! Also geh raus und mach etwas daraus!")

# Adding some more content
    st.markdown("""
    ### Willkommen bei HEALTHCOACH!
    #### Funktionen:

    - **Patientendatenbank**
      - Verwalte Patientendaten: EKGs und Leistungsanalysen

    - **Trainingsübersicht**
      - **Laufumfang:** Verfolge die Entwicklung deines Laufumfangs über die Zeit.

    - **Datei-Upload**
      - Lade deine `.fit`-Dateien hoch.
      - Nur `.fit`-Dateien werden unterstützt. Andere Formate sind nicht zulässig.

    - **Datenbank**
      - Die Trainingsdaten werden in einer SQLite-Datenbank gespeichert und verarbeitet.

    - **Visualisierung und Analyse**
      - **Diagramme:** Trainingsfortschritte  werden in übersichtlichen Diagrammen dargestellt.
      - **Datenansicht:** Greife auf detaillierte Informationen zu deinen Trainingseinheiten zu.

    #### Nutzung:

    1. **Datei hochladen:** Nutze den Datei-Upload-Bereich, um deine `.fit`-Dateien hochzuladen.
    2. **Übersicht prüfen:** Überprüfe deine Trainingsdaten.
    3. **Analyse ansehen:** Sieh dir die Diagramme und Datenansichten an, um deine Fortschritte zu verfolgen.

    Starte jetzt und lade deine Trainingsdaten hoch, um deine Fitnessreise zu verfolgen und zu optimieren!
                
    ### Mögliche Erweiterungen:
    1. Trainingsplanungs-Feature hinzufügen
    2. Login, Unterteilung der User in Trainer/in und Athlet/in; Trainer/in kann die Daten der Athlet/innen einsehen und Trainingsplanung vornehmen
    3. Athlet/in kann die eigenen Daten und Trainingsplan erstellt von Trainer/in einsehen
    4. Eingabe ermöglichen für Ruhe-HRV-Messungen (vorgenommen z.B. mit App Kubios HRV), und daraus Erholungsstatus ableiten
    5. Gewicht-Eingabe um auf grobe Schwankungen reagieren zu können
    6. Kommentarfeld bei Trainingseinheiten und Trainingsnutzen (aerob, anaerob, VO2max, Wettkampf...)
    7. Bisherige Bestleistungen (PBs) im Überblick darstellen

    """)
# Interactive motivational phrases
    phrases = [
        "Glaube an dich selbst und all das, was du bist. Wisse, dass in dir etwas ist, das größer ist als jedes Hindernis.",
        "Erfolg ist die Summe kleiner Anstrengungen, die Tag für Tag wiederholt werden.",
        "Die einzige Grenze für unsere Verwirklichung von morgen wird unsere Zweifel von heute sein.",
        "Gib niemals auf, denn der Anfang ist immer der schwerste. Halte durch, die besten Dinge kommen, wenn du es am wenigsten erwartest.",
        "Dein Potenzial ist unendlich. Mach jeden Tag einen Schritt vorwärts und du wirst erstaunt sein, wie weit du kommen kannst."
    ]

# Randomly choose a phrase when clicking the button
    if st.button('Motiviere mich!'):
        random_phrase = random.choice(phrases)
        st.write(f"Motivation des Tages: {random_phrase}")

elif option == "🏥Patientendatenbank":

    st.write("# PATIENTEN-DATENBANK")

    # Laden Sie die Personendaten
    person_data = pc.Person.load_person_data()

    # Legen Sie eine neue Liste mit den Personennamen an
    patients = pc.Person.get_person_list(person_data)
    patients.insert(0, "Wählen Sie einen Patienten aus")

    # Nutzen Sie ihre neue Liste anstelle der hard-gecodeten Lösung
    selected_patient = st.selectbox("Wählen Sie einen Patienten aus", options=patients, key="sbVersuchsperson")

    # Anlegen des Session State. Bild, wenn es kein Bild gibt
    if 'picture_path' not in st.session_state:
        st.session_state.picture_path = 'data/pictures/Patientendatenbank.jpg'

    # Überprüfen, ob ein tatsächlicher Patient ausgewählt wurde
    if selected_patient != "Wählen Sie einen Patienten aus":
        st.session_state.current_user = selected_patient
        person_data_dict = pc.Person.find_person_data_by_name(st.session_state.current_user)
        st.session_state.picture_path = person_data_dict["picture_path"]
        person_instance = pc.Person(person_data_dict)
    else:
        st.session_state.picture_path = 'data/pictures/Patientendatenbank.jpg'
        st.session_state.current_user = ""
        person_instance = None

    # Öffne das Bild und zeige es an
    image = Image.open(st.session_state.picture_path)
    #st.image(image, caption=st.session_state.current_user if 'current_user' in st.session_state else "" )

    # Geburtsjahr zur Bildunterschrift hinzufügen
    if person_instance is not None:
        name = f"{person_instance.firstname} {person_instance.lastname}"
        date_of_birth = person_instance.date_of_birth
        try:
            # Stellen Sie sicher, dass date_of_birth ein Integer ist
            birth_year = int(date_of_birth)
        except ValueError:
            birth_year = "Unbekannt"
        caption = f"{name} (Geburtsjahr: {birth_year})"
    else:
        caption = ""

    st.image(image, caption=caption)

    # Prüfen, ob ein Patient ausgewählt wurde und EKG-Tests laden
    if person_instance:
        ekg_tests = person_instance.ekg_tests

        if ekg_tests:
            ekg_objects = [ekg.EKGdata(ekg_test) for ekg_test in ekg_tests]
            ekg_options = ["Wählen Sie einen Test aus"] + [
                f"Test-ID {ekg_obj.id}; Datum: {ekg_obj.date}; Dauer: {ekg_obj.duration:.2f} s" for ekg_obj in ekg_objects]
        else:
            ekg_options = ["Noch keine EKG-Daten vorhanden"]
                  

        selected_ekg = st.selectbox("Wählen Sie einen EKG-Test aus", options=ekg_options)

        if selected_ekg != "Wählen Sie einen Test aus" and selected_ekg != "Noch keine EKG-Daten vorhanden":
            ekg_id = int(selected_ekg.split(" ")[1].replace(";", ""))
            ekg_data = ekg.EKGdata.load_by_id(ekg_id)

            if ekg_data:
                st.write(f"Durchschnittliche Herzfrequenz: {ekg_data.heartrate:.2f} bpm")
                st.write(f"Herzratenvariabilität: {ekg_data.hvr:.2f}")

                # Slider für Zeitbereich hinzufügen
                max_duration = float(ekg_data.df["Zeit in ms"].iloc[-1]) / 1000 # Maximaler Zeitpunkt in s
                min_duration = float(ekg_data.df["Zeit in ms"].iloc[0]) / 1000 # Minimaler Zeitpunkt in s
                #Zeitfenster für den Plot

                window = st.number_input("Wählen Sie ein Zeitfenster (in Sekunden):", min_value=10, max_value=60, value=30, step=10)

                start_time = st.slider(
                    "Wählen Sie den Startzeitpunkt für den Plot (in Sekunden):",
                    min_duration, max_duration - window, min_duration, 0.1 # Slider je nach Startzeitpunkt anwendbar
                )

                end_time = start_time + window
                st.write(f"Plot von {start_time:.1f} s bis {end_time:.1f} s")
                ekg_data.make_plot(start_time, end_time)

        else:
            st.write("Keine EKG-Daten gefunden.")
                
        
        # Prüfen, ob ein Patient ausgewählt wurde und Leistungstest laden
        intervall_tests = person_instance.intervall_tests

        if intervall_tests:
            intervall_test_option = ["Wählen Sie einen Test aus"] + [f"Test-ID {intervall_tests['id']}; Datum: {intervall_tests['date']}"]
        else:
            intervall_test_option = ["Noch kein Leistungstest vorhanden"]

        selected_intervall_test = st.selectbox("Wählen Sie einen Leistungstest aus", options=intervall_test_option)

        if selected_intervall_test != "Wählen Sie einen Test aus" and selected_intervall_test != "Noch kein Leistungstest vorhanden":
            intervall_test_id = int(selected_intervall_test.split(" ")[1].replace(";", ""))
            

            if intervall_tests["id"] == intervall_test_id:
                dateipfad = intervall_tests.get("result_link")

                df = pd.read_csv(dateipfad)
                max_hr = person_instance.max_hr
                analyze_button = st.button("Herzfrequenzanalyse durchführen")

                if analyze_button:
                    st.write("Maximale Herzfrequenz:", max_hr)
                    time_in_zones = pha.analyze_heart_rate(df, max_hr)
                    avg_performance_in_zones = pha.analyze_performance(df)
                    avg_performance_generel = df['PowerOriginal'].mean().round().astype(int)
                    max_performance_generel = df['PowerOriginal'].max().round().astype(int)

                    st.subheader('Zeit in HF-Zonen (in mm˸ss):')
                    st.write(time_in_zones)
                    st.subheader('Durchschnittliche Leistung in den Herzfrequenzzonen (in Watt):')
                    st.write(avg_performance_in_zones)
                    st.subheader('Durchschnittliche Leistung gesamt (in Watt):')
                    st.write(avg_performance_generel)
                    st.subheader('Maximale Leistung (in Watt):')
                    st.write(max_performance_generel)

                    time = df.index / 60

                    fig = go.Figure()

                    fig.add_trace(go.Scatter(x=time, y=df['HeartRate'], mode='lines', name='Heart Rate'))
                    fig.add_trace(go.Scatter(x=time, y=df['PowerOriginal'], mode='lines', name='Power'))

                    fig.add_hrect(y0=0, y1=0.6*max_hr, fillcolor="lightblue", opacity=0.2, line_width=0)
                    fig.add_hrect(y0=0.6*max_hr, y1=0.7*max_hr, fillcolor="lightgreen", opacity=0.2, line_width=0)
                    fig.add_hrect(y0=0.7*max_hr, y1=0.8*max_hr, fillcolor="yellow", opacity=0.2, line_width=0)
                    fig.add_hrect(y0=0.8*max_hr, y1=0.9*max_hr, fillcolor="orange", opacity=0.2, line_width=0)
                    fig.add_hrect(y0=0.9*max_hr, y1=1.0*max_hr, fillcolor="red", opacity=0.2, line_width=0)

                    fig.update_layout(
                        title="Leistung und Herzfrequenz über die Zeit",
                        xaxis_title='Dauer [min]',
                        yaxis_title='Herzfrequenz [bpm], Leistung [W]'
                    )

                    st.plotly_chart(fig)
                
                powercurve_button = st.button("Powercurve anzeigen")

                if powercurve_button:

                    # Funktion zur Konvertierung von Sekunden in mm:ss Format
                    def seconds_to_mmss(seconds):
                        minutes, seconds = divmod(seconds, 60)
                        return f"{minutes:02d}:{seconds:02d}"

                    # Berechnet die Powercurve
                    powercurve = cp.calc_powercurve(df)

                    # Zeitfenster in mm:ss Format konvertieren
                    powercurve['Time_Window_mmss'] = powercurve['Time_Window'].apply(seconds_to_mmss)

                    # Zeitpunkte in mm:ss Format konvertieren
                    desired_times = [1, 30, 60, 100, 300, 600, 1200]
                    xticks_mmss = [seconds_to_mmss(t) for t in desired_times]

                    # Filter powercurve für Marker-Daten
                    marker_data = powercurve[powercurve['Time_Window'].isin(desired_times)]

                    st.subheader('Powercurve')

                    # Zeitreihenplot erstellen
                    fig = px.line(powercurve, x='Time_Window_mmss', y='Power', title='Evaluation PowerCurve')

                    # Hinzufügen von Markern zu den spezifischen Zeitpunkten
                    fig.add_trace(go.Scatter(
                        x=marker_data['Time_Window_mmss'],
                        y=marker_data['Power'],
                        mode='markers',
                        marker=dict(color='red', size=8),
                        name='Specific values'
                    ))

                    # Setze die x-Achse auf die gewünschten Zeitpunkte
                    fig.update_xaxes(title_text='Duration [mm:ss]', tickvals=xticks_mmss)
                    fig.update_yaxes(title_text='Powercurve [W]')

                    # Aktualisiere die Layout-Einstellungen für die x-Achse
                    fig.update_layout(
                        xaxis=dict(
                            tickmode='array',
                            tickvals=xticks_mmss,
                            #ticktext=xticks_mmss,
                            tickangle=-45  # Winkel der x-Achsen-Beschriftungen, um Überlappung zu vermeiden
                        )
                    )

                    st.plotly_chart(fig)

elif option == "🏃Trainingsübersicht":
    # Auswahlmöglichkeiten in der Seitenleiste
    option = st.sidebar.radio("Trainingsübersicht", ["Entwicklung Laufumfang"])

    # Heutiges Datum ermitteln
    today = datetime.date.today()   

    # Startdatum für den Datepicker
    start_date = datetime.date(2024, 1, 1)
    
        # Abstand einfügen
    st.sidebar.markdown("---")  # Fügt eine Trennlinie ein

    user_id = tb.get_active_user_id()

    uploaded_files = st.sidebar.file_uploader("Upload .fit file", accept_multiple_files=True, key="file_uploader")
    

# Anzeige des letzten hochgeladenen FIT-Files
    if uploaded_files:
        last_uploaded_file = uploaded_files[-1]
        st.sidebar.info(f"Last uploaded file: {last_uploaded_file.name}")
    # SQLite-Datenbankverbindung
    conn = sqlite3.connect('fitfile_data.db')
    c = conn.cursor()

    if uploaded_files:
        tb.create_table()  # Tabelle erstellen, falls nicht vorhanden
        for uploaded_file in uploaded_files:
            if not uploaded_file.name.endswith('.fit'):
                st.error(f"Die Datei {uploaded_file.name} wird nicht unterstützt. Es werden nur .fit Dateien akzeptiert.")
                continue

            fit_parser = ff.FitFile(uploaded_file, user_id)
            insert_sql = fit_parser.get_insert_statement()
            if insert_sql:
                try:
                    c.execute(insert_sql)
                    conn.commit()
                    st.success(f"Daten aus {uploaded_file.name} erfolgreich in die Datenbank eingefügt.")
                except sqlite3.Error as e:
                    st.error(f"Fehler beim Einfügen der Daten in die Datenbank: {e}")
    

    st.sidebar.markdown("---")  # Fügt eine Trennlinie ein


    if option == "Entwicklung Laufumfang":

        if 'show_user_form' not in st.session_state:
            st.session_state.show_user_form = False

        if 'user_id' not in st.session_state:
            st.session_state.user_id = None 

        if 'show_delete_form' not in st.session_state:
            st.session_state.show_delete_form = False


        #neuen Nutzer anlegen
        st.sidebar.markdown("Trainingsübersicht: Wählen Sie eine*n Athlet*in aus:")
        user = st.sidebar.selectbox("Athlet*in auswählen:", tb.get_user())

        #Trennlinie
        st.sidebar.markdown("---")
        st.sidebar.write("Athleteten und Athletinnen verwalten:")

        new_user_button = st.sidebar.button("Neue/n Athlet/in anlegen")
        if new_user_button:
            st.session_state.show_user_form = True

        if st.session_state.show_user_form:
            st.session_state.show_user_form = True
            user_vorname = st.sidebar.text_input("Vornamen eingeben:")
            user_nachname = st.sidebar.text_input("Nachnamen eingeben:")
            user_geburtsdatum = st.sidebar.date_input("Geburtsdatum eingeben:",value=datetime.date(2000, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
            user_id = user_geburtsdatum.strftime('%Y%m%d')
            user_max_hr = st.sidebar.number_input("Maximale Herzfrequenz eingeben:", min_value=1, max_value=300, value=220, step=1)
            st.sidebar.markdown("Wenn die maximale HF nicht bekannt ist, kann die maximale HF als 220 - Lebensalter geschätzt werden.")
            if st.sidebar.button("Speichern"):
                tb.insert_user(user_id, user_vorname, user_nachname, user_geburtsdatum, user_max_hr)
                st.sidebar.success(f"Athlet/in {user_vorname} {user_nachname} erfolgreich angelegt.")
                st.session_state.show_user_form = False
        else:
            if user:
                user_id = user.split(" - ")[0]
                conn = sqlite3.connect('fitfile_data.db')
                c = conn.cursor()
                c.execute("UPDATE 'active_User' SET active_User = ?", (user_id,))
                conn.commit()

        
        delete_user_button = st.sidebar.button("Athlet/in löschen")
        if delete_user_button:
            st.session_state.show_delete_form = True

        if st.session_state.show_delete_form:     
            del_user = st.sidebar.selectbox("Athlet*in auswählen:", tb.get_user(), key = "del_user")
            user_id = user.split(" - ")[0]
            if st.sidebar.button("Löschen"):
                tb.delete_user(user_id)
                st.sidebar.success(f"Athlet:in {user} erfolgreich gelöscht.")


    
    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

    # Eindeutige Einschränkung hinzufügen
    create_unique_index_sql = """
    CREATE UNIQUE INDEX IF NOT EXISTS unique_activity ON trainings(activity_date, activity_duration);
    """
    c.execute(create_unique_index_sql)
    conn.commit()  # Änderungen speichern
    conn.close()

    # Daten aus der Datenbank abrufen und nach Kalenderwoche aggregieren
    df = tb.get_training_data()

    if df.size != 0:
        # Konvertiere activity_date-Spalte zu datetime
        df['activity_date'] = pd.to_datetime(df['activity_date']).dt.date

        # Aggregation der Daten nach Kalenderwoche
        df['activity_kw'] = pd.to_datetime(df['activity_date']).dt.isocalendar().week
        weekly_data = df.groupby('activity_kw')['total_distance'].sum().reset_index()

        # Berechnung der prozentualen Veränderung zwischen den Kalenderwochen
        weekly_data["Veränderung (%)"] = weekly_data["total_distance"].pct_change() * 100
        weekly_data["Veränderung (%)"] = weekly_data["Veränderung (%)"].fillna(0)  # Ersetze NaN mit 0 für den ersten Wert

        # Lineare Regression für die Trendlinie
        X = np.arange(len(weekly_data)).reshape(-1, 1)  # Kalenderwochen als Feature
        y = weekly_data["total_distance"].values  # Laufumfänge als Zielwert
        model = LinearRegression().fit(X, y)
        trend = model.predict(X)

        # Darstellung des Diagramms im Tab "Chart"
        tab1.subheader("Entwicklung Laufumfang")
        try:
            fig = go.Figure()
        except:
            st.write(f"Noch keine Tabelle vorhanden.")

        # Balkendiagramm
        fig.add_trace(go.Bar(
            x=weekly_data["activity_kw"],
            y=weekly_data["total_distance"],
            text=weekly_data["Veränderung (%)"].apply(lambda x: f'{x:.2f}%'),
            textposition='auto',
            name="Laufumfang"
        ))

        # Trendlinie
        fig.add_trace(go.Scatter(
            x=weekly_data["activity_kw"],
            y=trend,
            mode='lines',
            name='Trendlinie',
            line=dict(color='firebrick', width=2)
        ))

        fig.update_layout(
            title="Entwicklung des Laufumfangs mit prozentualer Veränderung",
            xaxis_title="Kalenderwoche",
            yaxis_title="Laufumfang (km)",
            template="plotly_white"
        )

        tab1.plotly_chart(fig)

        df_trainings_week = tb.get_training_data_by_week(tab1.number_input("Kalenderwoche eingeben:", min_value=1, max_value=53, value=1))

        #Säulendiagramm der trainings in der ausgewählten Woche
        fig2 = go.Figure(data=[
            go.Bar(name='total_distance', x=df_trainings_week['activity_date'], y=df_trainings_week['total_distance'], text=df_trainings_week['total_distance'], textposition='auto')
        ])
        fig2.update_layout(barmode='group', xaxis_tickangle=-45, title="Laufumfang pro Tag in der ausgewählten Kalenderwoche")
    
        tab1.plotly_chart(fig2)
        

        # Datepicker zur Auswahl eines Datums im angegebenen Zeitraum
        selected_date = tab2.date_input(
                "Wähle ein Datum aus:",
                (start_date, today),  # Standardmäßig von 1. Januar 2024 bis heute
                start_date,  # Standardwert ist der 1. Januar 2024
                today,  # Enddatum ist das heutige Datum
                format="DD.MM.YYYY"  # Format des Datumsinputs
            )
        # Anzeigen der Daten
        df_overview = tb.get_overview_data()

        try:
            if isinstance(selected_date, tuple):
                start_date = selected_date[0]  # Umwandlung in datetime.date
                end_date = selected_date[1]  # Umwandlung in datetime.date

                # Sicherstellen, dass activity_date im datetime.date-Format ist
                df_overview['activity_date'] = pd.to_datetime(df_overview['activity_date']).dt.date
                
                # Filtern der Datenframes nach dem ausgewählten Datumbereich
                df_selected = df_overview[(df_overview['activity_date'] >= start_date) & 
                                        (df_overview['activity_date'] <= end_date)]

                summary_data = tb.get_summary_data(start_date, end_date)

                tab2.write(df_selected)
                tab2.write(summary_data)

                #trennlinie 
                tab2.markdown("---")
                tab2.write("Trainingseinheit löschen:")
                try:
                # Löschen von Einträgen aus der Datenbank mit der activity_id
                    delete_id = tab2.number_input("Activity-ID des Trainings, das sie löschen wollen, auswählen:", min_value=0, max_value=53, value=1, key="delete_id")
                    if tab2.button("Löschen"):
                        tb.delete_entry(delete_id)
                except Exception as e:
                    tab2.write(f"Fehler beim Löschen! {e}")

                
            else:
                st.write("Bitte wählen Sie einen gültigen Zeitraum aus.")
        except Exception as e:
            tab2.write(f"Fehler - bitte gültigen Zeitraum auswählen! Verursachende Fehlermeldung: {e}")
    
    else:
        st.write("Noch keine Daten vorhanden.")
        tab2.write("Noch keine Daten vorhanden.")

try:
    if isinstance(selected_date, tuple):
        start_date = selected_date[0]  # Umwandlung in datetime.date
        end_date = selected_date[1]  # Umwandlung in datetime.date

        # Sicherstellen, dass activity_date im datetime.date-Format ist
        df_overview['activity_date'] = pd.to_datetime(df_overview['activity_date']).dt.date
        
        # Filtern der Datenframes nach dem ausgewählten Datumbereich
        df_selected = exp.filter_dataframe(df_overview, start_date, end_date)

        try:
            if tab2.button("Export all to CSV", help="Klicken Sie hier um die Daten als CSV zu exportieren!"):
                csv_path = exp.export_to_csv(df_selected)
                st.success(f"Data successfully exported to {csv_path}")
                st.experimental_rerun()
        except Exception as e:
            tab2.write(f"Fehler beim Exportieren als CSV! {e}")

        try:
            if tab2.button("Export all to PDF", help="Klicken Sie hier um die Daten als PDF zu exportieren!"):
                output_pdf_path = exp.export_to_pdf(df_selected)
                st.success(f"Data successfully exported to {output_pdf_path}")
        except Exception as e:
            tab2.write(f"Fehler beim Exportieren als PDF! {e}")

    else:
        tab2.write("Bitte wählen Sie einen gültigen Zeitraum aus.")
    #exception 
except Exception as e:
    tab2.write(f"Fehler - bitte gültigen Zeitraum auswählen! Verursachende Fehlermeldung: {e}")




        


        
    

        

        

