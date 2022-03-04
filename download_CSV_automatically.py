import time
from datetime import datetime
from urllib import request
import os

now = datetime.now()  # aktueller Zeitstempel JJJJ-MM-TT HH:MM.SS
# aktuelle Zeit als unix-Timestamp
timestamp = datetime.timestamp(datetime.now())
# Zeitstempel des Startdatums 25.09.2020 berechnen
zeitstempel = timestamp - 43804800
datum = datetime.fromtimestamp(zeitstempel).strftime('%Y-%m-%d')  # Datumsformat JJJJ-MM-TT festlegen

os.makedirs('./dht22_v2/') # Unterordner zur Speicherung von Temperatur- und Luftfeuchtigkeitssensor-Daten erstellen
os.makedirs('./sds011_v2/')  # Unterordner zur Speicherung von Feinstaubsensor-Daten erstellen

counter = 1

while zeitstempel <= 1632434400:
    print(counter)
    datum = datetime.fromtimestamp(zeitstempel).strftime('%Y-%m-%d')

    pfadServer = f'http://archive.sensor.community/{datum}/{datum}_sds011_sensor_3659.csv' # Server-URL
    pfadLokal = f'sds011/{datum}_sds011_sensor_3659.csv'  # Dateiname festlegen
    request.urlretrieve(pfadServer, pfadLokal)  # Download durchführen
    #time.sleep(1)
    pfadServer = f'http://archive.sensor.community/{datum}/{datum}_dht22_sensor_3660.csv'
    pfadLokal = f'dht22/{datum}_dht22_sensor_3660.csv'
    request.urlretrieve(pfadServer, pfadLokal)

    zeitstempel += 86400  # Zeitstempel um 1 Tag erhöhen

    counter += 1
    #if counter % 25 == 0:  # nach 25 Durchgängen 3sec Pause
    #    time.sleep(3)