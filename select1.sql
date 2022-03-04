SELECT MIN(xdh.humidity), MAX(xdh.humidity), AVG(xdh.humidity) 
  FROM dht22 xdh
 WHERE xdh.timestamp LIKE "2021-03-14%"