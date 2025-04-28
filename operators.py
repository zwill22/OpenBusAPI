import sqlite3
from tools import apiOutput

sqlite3.connect("bus_operators.db")

url = "https://www.travelinedata.org.uk/noc/api/1.0/nocrecords.xml"

output = apiOutput(url)

print(output)
