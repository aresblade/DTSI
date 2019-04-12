import datetime
import sqlite3
import unidecode
import itertools
import fuzzyMethods
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl

class FUZZY_OBJECT:
    def __init__(self, index, voltage, current, temperature, humidity, date, city, stationName):
        self.index = index
        self.voltage = voltage
        self.current = current
        self.temperature = temperature
        self.humidity = humidity
        self.date = date
        self.city = city
        self.stationName = stationName

fuzzy_object = []
fuzzy_object_filtered = []
fuzzy_values = ["low", "medium", "high", "critical"]
fuzzy_var_inputs = ["temperature", "voltage", "humidity"]
fuzzy_var_time = ['morning', 'midday', 'afternoon', 'evening', 'night']

#Generate all combinations of words 
def set_all_combinations():
    all_combinations = []
    tuples_list = list(itertools.product(fuzzy_values, fuzzy_var_inputs))

    for combination in tuples_list:
        all_combinations.append(' '.join(combination))

    return all_combinations

def read_request(string):
    request_values_list = []
    words_combinations = set_all_combinations()

    for combination in words_combinations:
        if combination in string:
            request_values_list.append(combination)

    # print(request_values_list)
    return request_values_list

def main():
    print("Welcome in fuzzy SQL")

    database = sqlite3.connect('jamedia.db')
    cursor = database.cursor()
    sql = "SELECT ID, VOLTAGE, CURRENT, TEMPERATURE, HUMIDITY, DATE, STATION_NAME, CITY FROM DANE INNER JOIN NAMES on NAMES.STATION_ID = DANE.STATION_ID"
   
    for row in cursor.execute(sql):
        fuzzy_object.append(FUZZY_OBJECT(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    request = input('Write request: ')

    sqlFiltered = sql + ' WHERE' + fuzzyMethods.getSpecificTable(read_request(request))

    for row in cursor.execute(sqlFiltered):
        fuzzy_object_filtered.append(FUZZY_OBJECT(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    

    # for row in read_request(request):
    #     print(row)
    temperature = np.arange(0, 11, 1)
    a = fuzz.trimf(temperature, [0, 0, 5])
    database.close()

if __name__ == '__main__':
    main()

# for voltage in cursor:
#usefull loop
# sql = "SELECT ID,STATION_ID,VOLTAGE,CURRENT,TEMPERATURE,HUMIDITY,datetime(DATE,'localtime') as DATE FROM DANE WHERE STATION_ID = "+str(station) + " ORDER BY " + orderby;