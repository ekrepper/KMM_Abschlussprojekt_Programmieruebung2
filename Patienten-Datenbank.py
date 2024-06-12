import streamlit as st
from PIL import Image
from person_class import Person as p
from ekg_class import EKGdata as ekg
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

#from A_my_streamlit import read_data as rd
from performance_hr_analysis import performance_hr_analysis as pha 
from my_functions import calc_powercurve as cp

# Eine Überschrift der ersten Ebene
st.write("# PATIENTEN-DATENBANK")

# Laden Sie die Personendaten
person_data = p.load_person_data()

# Legen Sie eine neue Liste mit den Personennamen an
patients = p.get_person_list(person_data)
patients.insert(0, "Wählen Sie einen Patienten aus")

# Nutzen Sie ihre neue Liste anstelle der hard-gecodeten Lösung
selected_patient = st.selectbox("Wählen Sie einen Patienten aus", options=patients, key="sbVersuchsperson")

# Anlegen des Session State. Bild, wenn es kein Bild gibt
if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/Patientendatenbank.jpg'

# Überprüfen, ob ein tatsächlicher Patient ausgewählt wurde
if selected_patient != "Wählen Sie einen Patienten aus":
    st.session_state.current_user = selected_patient
    person_data_dict = p.find_person_data_by_name(st.session_state.current_user)
    st.session_state.picture_path = person_data_dict["picture_path"]
    person_instance = p(person_data_dict)
else:
    st.session_state.picture_path = 'data/pictures/Patientendatenbank.jpg'
    st.session_state.current_user = ""
    person_instance = None

# Öffne das Bild und zeige es an
image = Image.open(st.session_state.picture_path)
st.image(image, caption=st.session_state.current_user if 'current_user' in st.session_state else "" )

# Prüfen, ob ein Patient ausgewählt wurde und EKG-Tests laden
if person_instance:
    ekg_tests = person_instance.ekg_tests

    if ekg_tests:
        ekg_options = ["Wählen Sie einen Test aus"] + [f"Test-ID {ekg['id']}; Datum: {ekg['date']}" for ekg in ekg_tests]
    else:
        ekg_options = ["Noch keine EKG-Daten vorhanden"]

    selected_ekg = st.selectbox("Wählen Sie einen EKG-Test aus", options=ekg_options)

    if selected_ekg != "Wählen Sie einen Test aus" and selected_ekg != "Noch keine EKG-Daten vorhanden":
        ekg_id = int(selected_ekg.split(" ")[1].replace(";", ""))
        ekg_data = ekg.load_by_id(ekg_id)

        if ekg_data:
            st.write(f"Durchschnittliche Herzfrequenz: {ekg_data.heartrate:.2f} bpm")
            ekg_data.make_plot()
        
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
                st.write(max_hr)
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

                        

