import requests
import schedule
import time
import threading

# Webhook-URL (deine angepasste URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1325851140859891915/Tzz4PtR7Fscu0X0fXzeRqToq0ctGJYRlU75F7uEHn256i-LBMAMz7-SBOFM1FKVBicRW"

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

# Funktion für Konsoleneingabe
def listen_for_command():
    while True:
        command = input("Gib einen Befehl ein: ").strip()
        if command == "!TIME-SKIP":
            print("TIME-SKIP erkannt. Sende Umfrage sofort...")
            send_poll()

# Zeitplan: Täglich um 10:00 Uhr
schedule.every().day.at("10:00").do(send_poll)

# Thread für Konsoleneingabe starten
thread = threading.Thread(target=listen_for_command, daemon=True)
thread.start()

print("Webhook-Bot läuft. Warte auf die geplante Zeit oder einen Konsolenbefehl...")

# Endlos-Loop, um den Zeitplan auszuführen
while True:
    schedule.run_pending()
    time.sleep(1)
