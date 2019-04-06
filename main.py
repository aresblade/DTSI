import datetime
import time
import sqlite3
import unidecode


database = sqlite3.connect('/home/jamedia/jamedia.db')
cursor = database.cursor()
sql = "SELECT VOLTAGE FROM DANE WHERE STATION_ID = "+ stationid +" AND ID IN (SELECT max(ID) FROM DANE GROUP BY STATION_ID) LIMIT 3;"
cursor.execute(sql)
for voltage in cursor:
	#usefull loop
sql = "SELECT ID,STATION_ID,VOLTAGE,CURRENT,TEMPERATURE,HUMIDITY,datetime(DATE,'localtime') as DATE FROM DANE WHERE STATION_ID = "+str(station) + " ORDER BY " + orderby;
database.close()
