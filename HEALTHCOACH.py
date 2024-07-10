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


# Set Streamlit page configuration
st.set_page_config(layout="centered", page_title="Sports & Health Database", page_icon="🏃‍♀️")

# Add a title to the sidebar for navigation
st.sidebar.title("🌐Navigation")

# Create a select box in the sidebar for page navigation options
option = st.sidebar.selectbox("Select a page:", ["🏠Home", "🏥Patientendatenbank", "🏃Trainingsübersicht"])

# Get the current directory of the file
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Get the parent directory
parentdir = os.path.dirname(currentdir)

# Insert the parent directory to the system path
sys.path.insert(0, parentdir)

# Check if the selected option is "🏠Home"
if option == "🏠Home":
        # Set the title for the Home page
    st.title = "🏠Home"
 
    # Additional page configuration for Home page
    page_title="Sports & Health Database",
    page_icon="⚕️",
    layout="centered",
    initial_sidebar_state="collapsed"


    # Apply custom CSS styling using markdown
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

    # Add header with animation using markdown
    st.markdown('<div class="header animate__animated animate__fadeInDown">HEALTHCOACH</div>', unsafe_allow_html=True)
    # Add subheader with animation using markdown
    st.markdown('<div class="subheader animate__animated animate__fadeInUp">Patienten- und Trainingsdaten im Überblick</div>', unsafe_allow_html=True)

    # Open and display an image
    image = Image.open("data/screenshots/HEALTHCOACH.png")

    # Example of centered content
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

    st.image(image, caption="", use_column_width=True)

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

    # Display main content with markdown
    st.markdown("""
    ### Willkommen bei HEALTHCOACH!
    #### Funktionen:

    - **Patientendatenbank**
      - Verwalte Patientendaten: EKGs und Leistungsanalysen

    - **Trainingsübersicht**
      - **Laufumfang:** Verfolge die Entwicklung deines Laufumfangs über die Zeit.

    - **Datei-Upload**
      - Lade deine .fit-Dateien hoch.
      - Nur .fit-Dateien werden unterstützt. Andere Formate sind nicht zulässig.
      - Bisher bietet HEALTHCOACH nur die Auswertung von Laufdaten an. Weitere Funktionen für weiter Sportarten sind in Planung.

    - **Datenbank**
      - Die Trainingsdaten werden in einer SQLite-Datenbank gespeichert und verarbeitet.

    - **Visualisierung und Analyse**
      - **Diagramme:** Trainingsfortschritte  werden in übersichtlichen Diagrammen dargestellt.
      - **Datenansicht:** Greife auf detaillierte Informationen zu deinen Trainingseinheiten zu.

    #### Nutzung:

    1. **Datei hochladen:** Nutze den Datei-Upload-Bereich, um deine .fit-Dateien hochzuladen.
    2. **Übersicht prüfen:** Überprüfe deine Trainingsdaten.
    3. **Analyse ansehen:** Sieh dir die Diagramme und Datenansichten an, um deine Fortschritte zu verfolgen.
    4. **Export der Daten:** Exportiere deine Daten als CSV oder PDF.

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
   # List of motivational phrases
    phrases = [
        "Glaube an dich selbst und all das, was du bist. Wisse, dass in dir etwas ist, das größer ist als jedes Hindernis.",
        "Erfolg ist die Summe kleiner Anstrengungen, die Tag für Tag wiederholt werden.",
        "Die einzige Grenze für unsere Verwirklichung von morgen wird unsere Zweifel von heute sein.",
        "Gib niemals auf, denn der Anfang ist immer der schwerste. Halte durch, die besten Dinge kommen, wenn du es am wenigsten erwartest.",
        "Dein Potenzial ist unendlich. Mach jeden Tag einen Schritt vorwärts und du wirst erstaunt sein, wie weit du kommen kannst."
    ]

    # Button to generate random motivational phrase
    if st.button('Motiviere mich!'):
        random_phrase = random.choice(phrases)
        st.write(f"Motivation des Tages: {random_phrase}")


# Check if the selected option is "🏥Patientendatenbank"
elif option == "🏥Patientendatenbank":
    # Write the heading for the Patientendatenbank section
    st.write("# PATIENTEN-DATENBANK")

    # Load the person data
    person_data = pc.Person.load_person_data()

    # Get list of patients
    patients = pc.Person.get_person_list(person_data)
    patients.insert(0, "Wählen Sie einen Patienten aus")

    # Selectbox to choose a patient
    selected_patient = st.selectbox("Wählen Sie einen Patienten aus", options=patients, key="sbVersuchsperson")

# Check if 'picture_path' is not in st.session_state
    if 'picture_path' not in st.session_state:
        # Set the initial value for 'picture_path'
        st.session_state.picture_path = 'data/pictures/Patientendatenbank.jpg'


    if selected_patient != "Wählen Sie einen Patienten aus":
        # Set current user in session state
        st.session_state.current_user = selected_patient
        # Find person data for selected patient
        person_data_dict = pc.Person.find_person_data_by_name(st.session_state.current_user)
        # Set picture_path in session state based on person data
        st.session_state.picture_path = person_data_dict["picture_path"]
        # Create person instance
        person_instance = pc.Person(person_data_dict)
    else:
        # Reset session state values if no patient selected
        st.session_state.picture_path = 'data/pictures/Patientendatenbank.jpg'
        st.session_state.current_user = ""
        person_instance = None

    # Load the image based on picture_path in session state
    image = Image.open(st.session_state.picture_path)
    #st.image(image, caption=st.session_state.current_user if 'current_user' in st.session_state else "" )

    # Initialize caption (Add birth year to the picture)
    if person_instance is not None:
        name = f"{person_instance.firstname} {person_instance.lastname}"
        date_of_birth = person_instance.date_of_birth
        try:
            birth_year = int(date_of_birth)
        except ValueError:
            birth_year = "Unbekannt"
        caption = f"{name} (Geburtsjahr: {birth_year})"
    else:
        caption = ""

    st.image(image, caption=caption)

    # Check if person_instance exists and get EKG tests
    if person_instance:
        ekg_tests = person_instance.ekg_tests

        if ekg_tests:
            ekg_objects = [ekg.EKGdata(ekg_test) for ekg_test in ekg_tests]
            ekg_options = ["Wählen Sie einen Test aus"] + [
                f"Test-ID {ekg_obj.id}; Datum: {ekg_obj.date}; Dauer: {ekg_obj.duration:.2f} s" for ekg_obj in ekg_objects]
        else:
            ekg_options = ["Noch keine EKG-Daten vorhanden"]
                  
        # Display select box for EKG tests
        selected_ekg = st.selectbox("Wählen Sie einen EKG-Test aus", options=ekg_options)

        # Check if a specific EKG test is selected and display its details and options
        if selected_ekg != "Wählen Sie einen Test aus" and selected_ekg != "Noch keine EKG-Daten vorhanden":
            ekg_id = int(selected_ekg.split(" ")[1].replace(";", ""))
            ekg_data = ekg.EKGdata.load_by_id(ekg_id)

            if ekg_data:
                st.write(f"Durchschnittliche Herzfrequenz: {ekg_data.heartrate:.2f} bpm")
                st.write(f"Herzratenvariabilität: {ekg_data.hvr:.2f}")

                # Add a slider for the time window
                max_duration = float(ekg_data.df["Zeit in ms"].iloc[-1]) / 1000 
                min_duration = float(ekg_data.df["Zeit in ms"].iloc[0]) / 1000 
        
                # Time window for the plot
                window = st.number_input("Wählen Sie ein Zeitfenster (in Sekunden):", min_value=10, max_value=60, value=30, step=10)

                # Start time slider for the plot
                start_time = st.slider(
                    "Wählen Sie den Startzeitpunkt für den Plot (in Sekunden):",
                    min_duration, max_duration - window, min_duration, 0.1 # Slider je nach Startzeitpunkt anwendbar
                )

                end_time = start_time + window
                st.write(f"Plot von {start_time:.1f} s bis {end_time:.1f} s")
                ekg_data.make_plot(start_time, end_time)

        else:
            st.write("Keine EKG-Daten gefunden.")
                
        # Check if a patient is selected and load interval tests
        intervall_tests = person_instance.intervall_tests

        if intervall_tests:
            intervall_test_option = ["Wählen Sie einen Test aus"] + [f"Test-ID {intervall_tests['id']}; Datum: {intervall_tests['date']}"]
        else:
            intervall_test_option = ["Noch kein Leistungstest vorhanden"]

        # Select box to choose an interval test
        selected_intervall_test = st.selectbox("Wählen Sie einen Leistungstest aus", options=intervall_test_option)

        # If a specific interval test is selected, load its data and perform analysis
        if selected_intervall_test != "Wählen Sie einen Test aus" and selected_intervall_test != "Noch kein Leistungstest vorhanden":
            intervall_test_id = int(selected_intervall_test.split(" ")[1].replace(";", ""))
            
            # Assuming interval_tests is a list of dictionaries where each dictionary contains test information
            if intervall_tests["id"] == intervall_test_id:
                dateipfad = intervall_tests.get("result_link")
                # Read CSV data
                df = pd.read_csv(dateipfad)
                # Get maximum heart rate of the person from person_instance
                max_hr = person_instance.max_hr
                # Button to trigger heart rate analysis
                analyze_button = st.button("Herzfrequenzanalyse durchführen")

                # If analyze button is clicked, perform analysis and display results
                if analyze_button:
                    st.write("Maximale Herzfrequenz:", max_hr)

                    # Perform heart rate analysis using health_analysis_module
                    time_in_zones = pha.analyze_heart_rate(df, max_hr)
                    avg_performance_in_zones = pha.analyze_performance(df)
                    avg_performance_generel = df['PowerOriginal'].mean().round().astype(int)
                    max_performance_generel = df['PowerOriginal'].max().round().astype(int)

                    # Display results
                    st.subheader('Zeit in HF-Zonen (in mm˸ss):')
                    st.write(time_in_zones)
                    st.subheader('Durchschnittliche Leistung in den Herzfrequenzzonen (in Watt):')
                    st.write(avg_performance_in_zones)
                    st.subheader('Durchschnittliche Leistung gesamt (in Watt):')
                    st.write(avg_performance_generel)
                    st.subheader('Maximale Leistung (in Watt):')
                    st.write(max_performance_generel)

                    # Create plot using Plotly for heart rate and power over time
                    time = df.index / 60

                    fig = go.Figure()

                    fig.add_trace(go.Scatter(x=time, y=df['HeartRate'], mode='lines', name='Heart Rate'))
                    fig.add_trace(go.Scatter(x=time, y=df['PowerOriginal'], mode='lines', name='Power'))

                    # Add color-coded rectangles for heart rate zones
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

                    # Display Plotly chart
                    st.plotly_chart(fig)

                # Button to display power curve if clicked
                powercurve_button = st.button("Powercurve anzeigen")

                if powercurve_button:

                    # Function to convert seconds to mm:ss format
                    def seconds_to_mmss(seconds):
                        minutes, seconds = divmod(seconds, 60)
                        return f"{minutes:02d}:{seconds:02d}"

                    # Calculate power curve
                    powercurve = cp.calc_powercurve(df)

                    # Convert time window to mm:ss format
                    powercurve['Time_Window_mmss'] = powercurve['Time_Window'].apply(seconds_to_mmss)

                    # Convert desired times to mm:ss format for x-axis ticks
                    desired_times = [1, 30, 60, 100, 300, 600, 1200]
                    xticks_mmss = [seconds_to_mmss(t) for t in desired_times]

                    # Filter powercurve for marker data
                    marker_data = powercurve[powercurve['Time_Window'].isin(desired_times)]

                    # Display Powercurve subheader
                    st.subheader('Powercurve')

                    # Create line plot for Powercurve
                    fig = px.line(powercurve, x='Time_Window_mmss', y='Power', title='Evaluation PowerCurve')

                    # Add markers for specific values
                    fig.add_trace(go.Scatter(
                        x=marker_data['Time_Window_mmss'],
                        y=marker_data['Power'],
                        mode='markers',
                        marker=dict(color='red', size=8),
                        name='Specific values'
                    ))

                    # Set x-axis to desired time points
                    fig.update_xaxes(title_text='Duration [mm:ss]', tickvals=xticks_mmss)
                    fig.update_yaxes(title_text='Powercurve [W]')

                    # Update layout settings for x-axis
                    fig.update_layout(
                        xaxis=dict(
                            tickmode='array',
                            tickvals=xticks_mmss,
                            #ticktext=xticks_mmss,
                            tickangle=-45  # Angle of x-axis labels to avoid overlap
                        )
                    )
                    # Display Plotly chart
                    st.plotly_chart(fig)


# Check if the selected option is "🏃Trainingsübersicht"
elif option == "🏃Trainingsübersicht":
    # Sidebar options for training overview
    option = st.sidebar.radio("Trainingsübersicht", ["Entwicklung Laufumfang"])

    # Get today's date
    today = datetime.date.today()   

    # Start date for the date picker
    start_date = datetime.date(2024, 1, 1)
    
    # Insert a separator
    st.sidebar.markdown("---")  # Fügt eine Trennlinie ein

    # Get active user ID
    user_id = tb.get_active_user_id()

    # File uploader for .fit files
    uploaded_files = st.sidebar.file_uploader("Upload .fit file", accept_multiple_files=True, key="file_uploader")
    

    # Display the last uploaded FIT file
    if uploaded_files:
        last_uploaded_file = uploaded_files[-1]
        st.sidebar.info(f"Last uploaded file: {last_uploaded_file.name}")
    # SQLite database connection
    conn = sqlite3.connect('fitfile_data.db')
    c = conn.cursor()

    # Process uploaded files
    if uploaded_files:
        tb.create_table()  
        for uploaded_file in uploaded_files:
            if not uploaded_file.name.endswith('.fit'):
                st.error(f"Die Datei {uploaded_file.name} wird nicht unterstützt. Es werden nur .fit Dateien akzeptiert.")
                continue

            # Parse the FIT file
            fit_parser = ff.FitFile(uploaded_file, user_id, int(tb.get_max_hr()))
            insert_sql = fit_parser.get_insert_statement()
            if insert_sql:
                try:
                    c.execute(insert_sql)
                    conn.commit()
                    st.success(f"Daten aus {uploaded_file.name} erfolgreich in die Datenbank eingefügt.")
                except sqlite3.Error as e:
                    st.error(f"Fehler beim Einfügen der Daten in die Datenbank: {e}")
    

    st.sidebar.markdown("---")  # Add separator line


    if option == "Entwicklung Laufumfang":
   # Initialize session state variables if not already defined
        if 'show_user_form' not in st.session_state:
            st.session_state.show_user_form = False

        if 'user_id' not in st.session_state:
            st.session_state.user_id = None 

        if 'show_delete_form' not in st.session_state:
            st.session_state.show_delete_form = False

        # Create a new user
        st.sidebar.markdown("Trainingsübersicht: Wählen Sie eine*n Athlet*in aus:")
        user = st.sidebar.selectbox("Athlet*in auswählen:", tb.get_user())

        # Add a separator
        st.sidebar.markdown("---")
        st.sidebar.write("Athleteten und Athletinnen verwalten:")

        # Button to create a new user
        new_user_button = st.sidebar.button("Neue/n Athlet/in anlegen")
        if new_user_button:
            st.session_state.show_user_form = True

        # Display form to create a new user if button is clicked
        if st.session_state.show_user_form:
            st.session_state.show_user_form = True
            user_vorname = st.sidebar.text_input("Vornamen eingeben:")
            user_nachname = st.sidebar.text_input("Nachnamen eingeben:")
            user_geburtsdatum = st.sidebar.date_input("Geburtsdatum eingeben:",value=datetime.date(2000, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
            user_id = user_geburtsdatum.strftime('%Y%m%d')
            user_max_hr = st.sidebar.number_input("Maximale Herzfrequenz eingeben:", min_value=1, max_value=300, value=220, step=1)
            st.sidebar.markdown("Wenn die maximale HF nicht bekannt ist, kann die maximale HF als 220 - Lebensalter geschätzt werden.")
            # Button to save new user
            if st.sidebar.button("Speichern"):
                tb.insert_user(user_id, user_vorname, user_nachname, user_geburtsdatum, user_max_hr)
                st.sidebar.success(f"Athlet/in {user_vorname} {user_nachname} erfolgreich angelegt.")
                st.session_state.show_user_form = False
        else:
            # Update active user if a user is selected
            if user:
                user_id = user.split(" - ")[0]
                conn = sqlite3.connect('fitfile_data.db')
                c = conn.cursor()
                c.execute("UPDATE 'active_User' SET active_User = ?", (user_id,))
                conn.commit()

        # Button to delete a user
        delete_user_button = st.sidebar.button("Athlet/in löschen")
        if delete_user_button:
            st.session_state.show_delete_form = True

        # Display form to delete a user if button is clicked
        if st.session_state.show_delete_form:     
            del_user = st.sidebar.selectbox("Athlet*in auswählen:", tb.get_user(), key = "del_user")
            user_id = user.split(" - ")[0]
            if st.sidebar.button("Löschen"):
                tb.delete_user(user_id)
                st.sidebar.success(f"Athlet:in {user} erfolgreich gelöscht.")


    
    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

    # Add a unique constraint
    create_unique_index_sql = """
    CREATE UNIQUE INDEX IF NOT EXISTS unique_activity ON trainings(activity_date, activity_duration);
    """
    c.execute(create_unique_index_sql)
    conn.commit()  # Änderungen speichern
    conn.close()

    # Retrieve data from the database and aggregate by calendar week
    df = tb.get_training_data()

    if df.size != 0:
        # Convert activity_date column to datetime
        df['activity_date'] = pd.to_datetime(df['activity_date']).dt.date

        # Aggregate data by calendar week
        df['activity_kw'] = pd.to_datetime(df['activity_date']).dt.isocalendar().week
        weekly_data = df.groupby('activity_kw')['total_distance'].sum().reset_index()

        # Calculate percentage change between calendar weeks
        weekly_data["Veränderung (%)"] = weekly_data["total_distance"].pct_change() * 100
        weekly_data["Veränderung (%)"] = weekly_data["Veränderung (%)"].fillna(0)  # Ersetze NaN mit 0 für den ersten Wert

        # Linear regression for trend line
        X = np.arange(len(weekly_data)).reshape(-1, 1)  # Kalenderwochen als Feature
        y = weekly_data["total_distance"].values  # Laufumfänge als Zielwert
        model = LinearRegression().fit(X, y)
        trend = model.predict(X)

        # Display the chart in the "Chart" tab
        tab1.subheader("Entwicklung Laufumfang")
        try:
            fig = go.Figure()
        except:
            st.write(f"Noch keine Tabelle vorhanden.")

        # Bar chart
        fig.add_trace(go.Bar(
            x=weekly_data["activity_kw"],
            y=weekly_data["total_distance"],
            text=weekly_data["Veränderung (%)"].apply(lambda x: f'{x:.2f}%'),
            textposition='auto',
            name="Laufumfang"
        ))

        # Trend line
        fig.add_trace(go.Scatter(
            x=weekly_data["activity_kw"],
            y=trend,
            mode='lines',
            name='Trendlinie',
            line=dict(color='firebrick', width=2)
        ))

        # layout adjustments
        fig.update_layout(
            title="Entwicklung des Laufumfangs mit prozentualer Veränderung",
            xaxis_title="Kalenderwoche",
            yaxis_title="Laufumfang (km)",
            template="plotly_white"
        )

        # Plotly chart in Streamlit
        tab1.plotly_chart(fig)
    
        # Get training data for the specified calendar week
        df_trainings_week = tb.get_training_data_by_week(tab1.number_input("Kalenderwoche eingeben:", min_value=1, max_value=53, value=1))

        # Plot bar chart of training data for the selected week
        fig2 = go.Figure(data=[
            go.Bar(name='total_distance', x=df_trainings_week['activity_date'], y=df_trainings_week['total_distance'], text=df_trainings_week['total_distance'], textposition='auto')
        ])
        fig2.update_layout(barmode='group', xaxis_tickangle=-45, title="Laufumfang pro Tag in der ausgewählten Kalenderwoche")
    
        tab1.plotly_chart(fig2)
        

        # Datepicker to select a date within the specified range
        selected_date = tab2.date_input(
                "Wähle ein Datum aus:",
                (start_date, today),  # Default from January 1, 2024 to toda
                start_date,  # Default is January 1, 2024
                today,  # End date is today
                format="DD.MM.YYYY"  # Date input format
            )
        # Retrieve overview data
        df_overview = tb.get_overview_data()

        try:
            if isinstance(selected_date, tuple):
                start_date = selected_date[0]  # Convert to datetime.date
                end_date = selected_date[1]  # Convert to datetime.date

                # Ensure activity_date is in datetime.date format
                df_overview['activity_date'] = pd.to_datetime(df_overview['activity_date']).dt.date
                
                # Filter dataframe by selected date range
                df_selected = df_overview[(df_overview['activity_date'] >= start_date) & 
                                        (df_overview['activity_date'] <= end_date)]

                summary_data = tb.get_summary_data(start_date, end_date)

                tab2.write(df_selected)
                tab2.write(summary_data)

                # Add separator line
                tab2.markdown("---")
                # Delete training entry
                tab2.write("Trainingseinheit löschen:")
                try:
                    delete_id = tab2.number_input("Activity-ID des Trainings, das sie löschen wollen, auswählen:", min_value=0, max_value=53, value=1, key="delete_id")
                    if tab2.button("Löschen"):
                        tb.delete_entry(delete_id)
                except Exception as e:
                    tab2.write(f"Fehler beim Löschen! {e}")

                # Add separator line
                tab2.markdown("---")
                 
            else:
                st.write("Bitte wählen Sie einen gültigen Zeitraum aus.")
        except Exception as e:
            tab2.write(f"Fehler - bitte gültigen Zeitraum auswählen! Verursachende Fehlermeldung: {e}")
    
    else:
        st.write("Noch keine Daten vorhanden.")
        tab2.write("Noch keine Daten vorhanden.")

    try:
        if isinstance(selected_date, tuple):
            start_date = selected_date[0]  # Convert to datetime.date
            end_date = selected_date[1]  # Convert to datetime.date

            # Ensure activity_date is in datetime.date format
            df_overview['activity_date'] = pd.to_datetime(df_overview['activity_date']).dt.date
            
            # Filter dataframe by selected date range
            df_selected = exp.filter_dataframe(df_overview, start_date, end_date)
            

            try:
                # Export selected data to CSV
                if tab2.button("Export all to CSV", help="Klicken Sie hier um die Daten als CSV zu exportieren!"):
                    csv_path = exp.export_to_csv(df_selected)
                    st.success(f"Data successfully exported to {csv_path}")
                    st.experimental_rerun() # Rerun Streamlit to reflect changes if necessary
            except Exception as e:
                tab2.write(f"Fehler beim Exportieren als CSV! {e}")
            

            try:
                # Export selected data to PDF  
                if tab2.button("Export all to PDF", help="Klicken Sie hier um die Daten als PDF zu exportieren!"):
                    output_pdf_path = exp.export_to_pdf(df_selected, summary_data)
                    st.success(f"Data successfully exported to {output_pdf_path}")
            except Exception as e:
                tab2.write(f"Fehler beim Exportieren als PDF! {e}")

        else:
            tab2.write("Bitte wählen Sie einen gültigen Zeitraum aus.")
        #exception 
    except Exception as e:
        tab2.write(f"Fehler - bitte gültigen Zeitraum auswählen! Verursachende Fehlermeldung: {e}")