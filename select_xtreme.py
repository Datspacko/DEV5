import sqlite3
from unittest import result
dbname = "feinstaubstation"
select = "SELECT AVG(xfilt.humidity), AVG(xdh1.temperature) FROM dht22 xdh1, (SELECT xdh2.humidity, xdh2.timestamp FROM dht22 xdh2 WHERE xdh2.humidity <> 1 AND xdh2.humidity <> 99.9) AS xfilt WHERE xdh1.timestamp LIKE '2021-12-26%' AND xfilt.timestamp LIKE '2021-12-26%' AND xdh1.timestamp = xfilt.timestamp"

con = sqlite3.connect(dbname)
c = con.cursor()
c.execute(select)

results = c.fetchall()
print(results)
