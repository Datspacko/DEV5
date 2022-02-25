import sqlite3
from csv import reader
from os import times
from time import time

import time
from datetime import datetime
from urllib import request
import os

now = datetime.now()
timestamp = datetime.timestamp(datetime.now())
zeitstempel = timestamp - 43804800
datum = datetime.fromtimestamp(zeitstempel).strftime('%Y-%m-%d')

conn = sqlite3.connect("feinstaubstation_2.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS sds011(sensor_ID int, sensor_type varchar(5), location int, lat decimal(5,3), lon decimal(5,3), timestamp varchar(20), P1 decimal(4,2), durP1 decimal(4,2), ratioP1 decimal(4,2), P2 decimal(4,2), durP2 decimal(4,2), ratioP2 decimal(4,2))""")
c.execute("""CREATE TABLE IF NOT EXISTS dht22 (sensor_ID int, sensor_type varchar(5), location int, lat decimal(5,3), lon decimal(5,3), timestamp varchar(20), temperature decimal(4,2), humidity decimal(4,2))""")

while zeitstempel <= 1632434400:
    datum = datetime.fromtimestamp(zeitstempel).strftime('%Y-%m-%d')
    zeitstempel += 86400  # Zeitstempel um 1 Tag erhöhen

    with open(f'sds011/{datum}_sds011_sensor_3659.csv', 'r') as csv_file:
        csv_reader = reader(csv_file, delimiter=';')
        list_sds011 = list(csv_reader)
        # print(list_sds011)

    for sensor_ID, sensor_type, location, lat, lon, timestamp, P1, durP1, ratioP1, P2, durP2, ratioP2 in list_sds011:
        print("Füge Daten hinzu:", sensor_ID, sensor_type, location, lat, lon, timestamp, P1, durP1, ratioP1, P2, durP2, ratioP2)
        c.execute("INSERT INTO sds011 (sensor_ID, sensor_type, location, lat, lon, timestamp, P1, durP1, ratioP1, P2, durP2, ratioP2) VALUES(:sensor_ID,:sensor_type,:location,:lat,:lon,:timestamp,:P1,:durP1,:ratioP1,:P2,:durP2,:ratioP2)", {'sensor_ID': sensor_ID, 'sensor_type': sensor_type, 'location': location, 'lat': lat, 'lon': lon, 'timestamp': timestamp, 'P1': P1, 'durP1': durP1, 'ratioP1': ratioP1, 'P2': P2, 'durP2': durP2, 'ratioP2': ratioP2})

    with open(f'dht22/{datum}_dht22_sensor_3660.csv', 'r') as csv_file:
        csv_reader = reader(csv_file, delimiter=';')
        list_dht22 = list(csv_reader)
        # print(list_dht22)

    for sensor_ID, sensor_type, location, lat, lon, timestamp, temperature, humidity in list_dht22:
        print("Füge Daten hinzu:", sensor_ID, sensor_type, location, lat, lon, timestamp, temperature, humidity)
        c.execute("INSERT INTO dht22 (sensor_ID, sensor_type, location, lat, lon, timestamp, temperature, humidity) VALUES(:sensor_ID,:sensor_type,:location,:lat,:lon,:timestamp,:temperature,:humidity)", {'sensor_ID': sensor_ID, 'sensor_type': sensor_type, 'location': location, 'lat': lat, 'lon': lon, 'timestamp': timestamp, 'temperature': temperature, 'humidity': humidity})

c.execute("""DELETE FROM sds011 WHERE timestamp = 'timestamp'""")
c.execute("""ALTER TABLE sds011 DROP COLUMN sensor_ID""")
c.execute("""ALTER TABLE sds011 DROP COLUMN sensor_type""")
c.execute("""ALTER TABLE sds011 DROP COLUMN location""")
c.execute("""ALTER TABLE sds011 DROP COLUMN lat""")
c.execute("""ALTER TABLE sds011 DROP COLUMN lon""")
c.execute("""ALTER TABLE sds011 DROP COLUMN durP1""")
c.execute("""ALTER TABLE sds011 DROP COLUMN ratioP1""")
c.execute("""ALTER TABLE sds011 DROP COLUMN durP2""")
c.execute("""ALTER TABLE sds011 DROP COLUMN ratioP2""")
c.execute("""DELETE FROM dht22 WHERE timestamp = 'timestamp'""")
c.execute("""ALTER TABLE dht22 DROP COLUMN sensor_id""")
c.execute("""ALTER TABLE dht22 DROP COLUMN sensor_type""")
c.execute("""ALTER TABLE dht22 DROP COLUMN location""")
c.execute("""ALTER TABLE dht22 DROP COLUMN lat""")
c.execute("""ALTER TABLE dht22 DROP COLUMN lon""")
conn.commit()
conn.close()