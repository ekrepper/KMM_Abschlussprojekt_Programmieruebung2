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
    st.markdown('<div class="header animate__animated animate__fadeInDown">Welcome to VIECHCOACH</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader animate__animated animate__fadeInUp">Wir machen ein wahres VIECH aus Dir!</div>', unsafe_allow_html=True)

    image = Image.open("data/screenshots/logosw.jpg")
    st.image(image, caption="Die 3 Creators (Lisi, Markus, Anna)")

    # Animated button
    #st.markdown('<button class="bounce-button">Get Started</button>', unsafe_allow_html=True)

    # Adding some interactivity
    if st.button('Get Started'):
        # Add a progress bar
        st.write("Your progress is our progress")
        progress_bar = st.progress(0)

        for percent_complete in range(100):
            time.sleep(0.1)  # Simulate a long computation
            progress_bar.progress(percent_complete + 1)
        
    # Adding a delay to simulate loading
        time.sleep(2)
    # Display the prompt after loading
        st.write("Du hast geklickt, gewartet und... nichts ist passiert! Eine App allein wird keine Wunder vollbringen - für deine Fitness bist du selbst verantwortlich! Also geh raus und mach etwas daraus!")

    # Adding some more content
    st.markdown("""
    ### Unser Ziel:
    - **Dein Herz so stark zu machen, wie das eines Blauwals!** 
    - **Deine Ausdauer so auf Vordermann zu bringen, wie die eines Dromedars!**
    - **Dich schnell zu machen, wie ein Gepard!**
    - **Sodass du ein Allesfresser werden kannst, wie ein Wildschwein!**
    """)
    
    #st.logo('HEALTHCOACH.png')

    st.markdown("""
    #### Mit dieser App wirst auch du zum Viech! 
    ###### Füttere in der linken Seitenleiste der Trainingsübersicht deine Trainingsdaten und lasse dein inneres Viech wachsen!
    """)

   
    # Adding some fun motivational quotes
    st.markdown("""
    **Motivationszitate:**
    - "Ein Löwe läuft nie einfach nur aus Spaß – er hat immer ein Ziel!" 🦁
    - "Beweg dich wie ein Affe im Dschungel und spüre die Freiheit!" 🐒
    - "Sei zäh wie ein Bär, stark wie ein Stier und schnell wie ein Gepard!" 🐻🐂🐆
    """)

    # Adding some fun facts
    st.markdown("""
    **Fun Facts:**
    - Wusstest du, dass ein Kolibri bis zu 70 Mal pro Sekunde mit den Flügeln schlägt? 🐦
    - Ein Gepard kann in nur 3 Sekunden von 0 auf 100 km/h beschleunigen! 🐆
    - Kängurus können nicht rückwärts springen – aber das wirst du mit deinem Training auch nicht müssen! 🦘
    """)

    # Additional humorous encouragement with interaction
    st.markdown("""
    **Zusätzliche Motivation:**
    - "Wenn du dich wie ein Faultier fühlst, erinnere dich daran: Selbst Faultiere erreichen ihr Ziel – langsam, aber sicher!" 🦥
    - "Schwitze wie ein Schwein – aber nicht im Schlamm!" 🐷
    - "Vergiss nicht: Ein gesundes Leben ist ein glückliches Leben – und du wirst zum Viech, das alles schafft!" 💪
    """)

    # Interactive funny phrases
    phrases = [
        "Wie ein Schwein im Trüffelrausch – finde dein inneres Trainingsziel und gib alles! 🐷",
        "Ein Wildschwein rennt durch den Wald und lässt sich nicht aufhalten – so wirst auch du mit deinem Training unaufhaltsam! 🐗",
        "Ein Schwein kann dich nicht inspirieren? Dann stell dir vor, wie schnell du bist, wenn du vor einem ausgewachsenen 200-Kilo-Schwein weglaufen willst!",
        "Es ist Zeit, den inneren Schweinehund zu besiegen und sich wie ein echtes Wildschwein zu fühlen! 🐽",
        "Vom Büroschwein zum Wildschwein: Diese App wird dich verwandeln!"
    ]

    # Randomly choose a phrase when clicking the button
    if st.button('Motiviere mich noch mehr!'):
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

        if option == "Entwicklung Laufumfang":
        # Heutiges Datum ermitteln
            today = datetime.date.today()

            # Startdatum für den Datepicker
            start_date = datetime.date(2024, 1, 1)
            
                # Abstand einfügen
            st.sidebar.markdown("---")  # Fügt eine Trennlinie ein

            uploaded_files = st.sidebar.file_uploader("Upload .fit file", accept_multiple_files=True, key="file_uploader")
            st.sidebar.caption("Choose a .fit file")

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
                    fit_parser = ff.FitFile(uploaded_file)
                    insert_sql = fit_parser.get_insert_statement()
                    if insert_sql:
                        try:
                            c.execute(insert_sql)
                            conn.commit()
                            st.success(f"Daten aus {uploaded_file.name} erfolgreich in die Datenbank eingefügt.")
                        except sqlite3.Error as e:
                            st.error(f"Fehler beim Einfügen der Daten in die Datenbank: {e}")

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

                    
                else:
                    st.write("Bitte wählen Sie einen gültigen Zeitraum aus.")
            except Exception as e:
                tab2.write(f"Fehler - bitte gültigen Zeitraum auswählen! Fehler: {str(e)}")