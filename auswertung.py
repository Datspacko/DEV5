import sqlite3
import time

jahr = input("Jahr eingeben: ")
monat = input("Monat eingeben: ")
tag = input("Tag eingeben: ")
datum = jahr + "-" + monat + "-" + tag

dbname = "feinstaubstation.db"
q1 = f"""
SELECT MIN(xfilt.humidity),  AVG(xfilt.humidity),  MAX(xfilt.humidity),
       MIN(xdh1.temperature),AVG(xdh1.temperature),MAX(xdh1.temperature)
  FROM dht22 xdh1, 
       (SELECT xdh2.humidity, xdh2.timestamp 
          FROM dht22 xdh2 
         WHERE xdh2.humidity <> 1 AND xdh2.humidity <> 99.9) AS xfilt 
 WHERE xdh1.timestamp = xfilt.timestamp
   AND xdh1.timestamp LIKE '{datum}%' 
   AND xfilt.timestamp LIKE '{datum}%'
"""

q2 = f"""
SELECT MIN(P1),AVG(P1),MAX(P1),
       MIN(P2),AVG(P2),MAX(P2)
  FROM sds011
 WHERE timestamp LIKE '{datum}%'
"""

# print("Query1: " + q1)
# print("Query2: " + q2)
# time.sleep(10)

con = sqlite3.connect(dbname)
c = con.cursor()
c.execute(q1)
results = c.fetchall()
out = str(results[0])
x1 = out.split(",")
print(x1[1])
