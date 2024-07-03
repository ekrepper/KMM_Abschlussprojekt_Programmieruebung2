# KMM_Abschlussprojekt_Programmieruebung2
### Clonen des Github-Repository auf den PC:

    Öffne Git Bash, navigieren zu dem gewünschten Ordner: cd "<gewünschter Ordner>"
    Repository in Ordner klonen: git clone
    Öffnen Ordner in VS Code

### Virtuellen Bereich erstellen:

    Öffnen eines neues Terminals --> windows Powershell
    Folgender Befehl erstellt einen Virtuellen Bereich: python -m venv .venv
    Folgender Befehl ein aktiviert Virtuellen Bereich: .venv\Scripts\Activate
    Falls dieser nicht funktioniert: Zugriff erlauben: Set-ExecutionPolicy RemoteSigned Scope CurrentUser
    Der Virtuelle Bereich ist nun erstellt und aktiviert

### Nötigen Pakete installieren:

    Nötige Pakete sind in der Text-Datei requirements.txt angeführt
    Alle Pakete gleichzeitig installieren: pip install -r requirements.txt (in Komandozeile von Windows Powershell)

### App starten:

    Mit dem Befehl streamlit run .\Patienten-Datenbank.py startet die App

### Funktionalitäten der App:

    - Home-Seite (🏠Home): Begrüßung und Motivation, um Nutzer zu sportlicher Aktivität zu inspirieren. Verwendung von Animationen und Zitaten, um die Benutzererfahrung zu verbessern.

    - Patientendatenbank-Seite (🏥Patientendatenbank): Ermöglicht die Auswahl und Anzeige von Patientendaten, einschließlich Herzfrequenzanalysen und Leistungskurven.

    - Trainingsübersicht-Seite (🏃Trainingsübersicht): Zeigt die Entwicklung des Laufumfangs über Wochen anhand von Diagrammen und ermöglicht die Auswahl von Datumsspannen zur detaillierten Anzeige von Trainingsdaten. Neue .Fit Dateinen können über den drag & drop Button hinzugefügt werden.