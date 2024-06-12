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
    alle Pakete gleichzeitig installieren: pip install -r requirements.txt (in Komandozeile von Windows Powershell)