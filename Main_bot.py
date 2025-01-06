import requests
import schedule
import time
import threading
from flask import Flask, render_template, redirect, url_for

# Webhook-URL (deine angepasste URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1325851140859891915/Tzz4PtR7Fscu0X0fXzeRqToq0ctGJYRlU75F7uEHn256i-LBMAMz7-SBOFM1FKVBicRW"

# Flask App initialisieren
app = Flask(__name__)

# Funktion zum Senden der Umfrage
def send_poll():
    payload = {
        "content": "/poll question:Wer ist on? choices:yes,no results:When the poll ends buttons:Yes time:9"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("Umfrage erfolgreich gesendet!")
        else:
            print(f"Fehler beim Senden: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Flask-Routen für das Webinterface
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_poll', methods=['POST'])
def send_poll_route():
    send_poll()
    return redirect(url_for('index'))  # Nach dem Absenden zurück zur Hauptseite

# Zeitplan: Täglich um 10:00 Uhr
schedule.every().day.at("10:00").do(send_poll)

# Thread für Flask-Server starten
def run_flask():
    app.run(debug=True, use_reloader=False)

# Thread für Konsoleneingabe starten
def listen_for_command():
    while True:
        command = input("Gib einen Befehl ein: ").strip()
        if command == "!TIME-SKIP":
            print("TIME-SKIP erkannt. Sende Umfrage sofort...")
            send_poll()

# Flask Server in separatem Thread starten
thread_flask = threading.Thread(target=run_flask, daemon=True)
thread_flask.start()

# Konsolenbefehl-Thread starten
thread_command = threading.Thread(target=listen_for_command, daemon=True)
thread_command.start()

print("Webhook-Bot läuft. Warte auf die geplante Zeit oder einen Konsolenbefehl...")

# Endlos-Loop, um den Zeitplan auszuführen
while True:
    schedule.run_pending()
    time.sleep(1)
