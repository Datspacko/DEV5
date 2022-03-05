import sqlite3
from unittest import result
dbname = "feinstaubstation.db"
query = """SELECT MIN(xdh.humidity), MAX(xdh.humidity), AVG(xdh.humidity) 
             FROM dht22 xdh
            WHERE xdh.timestamp LIKE '2021-03-14%'"""

con = sqlite3.connect(dbname)
c = con.cursor()
c.execute(query)

results = c.fetchall()
print(results)
print("ENDE")
