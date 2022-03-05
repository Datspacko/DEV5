import sqlite3
from unittest import result

jahr = input("Jahr eingeben: ")
monat = input("Monat eingeben: ")
tag = input("Tag eingeben: ")
datum = jahr + "-" + monat + "-" + tag

dbname = "feinstaubstation.db"
q1 = "SELECT MAX(xdh.temperature) "
q2 = "  FROM dht22 xdh"
q3 = " WHERE xdh.timestamp LIKE '" + datum + "%' "

query = q1+q2+q3

con = sqlite3.connect(dbname)
c = con.cursor()
c.execute(query)

results = c.fetchall()
out = "XXX" + str(results) + "XXX"
print(out)
