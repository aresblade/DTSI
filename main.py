import datetime
import sqlite3
import unidecode
import itertools
import fuzzyMethods
from prettytable import PrettyTable
import skfuzzy as fuzz
import numpy as np
import re, csv, sys
import os
import glob
import csv
from xlsxwriter.workbook import Workbook

from skfuzzy import control as ctrl

class FUZZY_OBJECT:
    def __init__(self, index, voltage, current, temperature, humidity, date, city, stationName, time):
        self.index = index
        self.voltage = voltage
        self.current = current
        self.temperature = temperature
        self.humidity = humidity
        self.date = date
        self.city = city
        self.stationName = stationName
        self.time = time

fuzzy_object = []
fuzzy_object_filtered = []
fuzzy_values = ["low", "medium", "high", "critical"]
fuzzy_var_inputs = ["temperature", "voltage", "humidity"]
fuzzy_var_time = ['morning', 'midday', 'afternoon', 'evening', 'night']

def pretty_table_to_tuples(input_str):
    lines = input_str.split("\n")
    num_columns = len(re.findall("\+", lines[0])) - 1
    line_regex = r"\|" + (r" +(.*?) +\|"*num_columns)
    for line in lines:
        m = re.match(line_regex, line.strip())
        if m:
            yield m.groups()

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
    for obj in fuzzy_var_time:
        words_combinations.append(obj)

    for combination in words_combinations:
        if combination in string:
            request_values_list.append(combination)

    # print(request_values_list)
    return request_values_list

def main():
    table = PrettyTable()
    print("Welcome in fuzzy SQL")

    database = sqlite3.connect('jamedia.db')
    cursor = database.cursor()
    sql = "SELECT ID, VOLTAGE, CURRENT, TEMPERATURE, HUMIDITY, DATE, STATION_NAME, CITY, strftime('%H:%M:%S', date) as Time FROM DANE INNER JOIN NAMES on NAMES.STATION_ID = DANE.STATION_ID"
   
    # for row in cursor.execute(sql):
    #     fuzzy_object.append(FUZZY_OBJECT(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    request = input('Write request: ')

    fuzzyValues = fuzzyMethods.getSpecificTable(read_request(request))
    sqlRequst = ''
    if (len(fuzzyValues) == 0):
        sqlRequst = sql
    else:
        sqlRequst = sql + ' WHERE' + fuzzyValues

    sqlRequst = sqlRequst + ' limit 15'

    field_names =  ['ID', 'VOLTAGE', 'CURRENT', 'TEMPERATURE', 'HUMIDITY', 'DATE', 'STATION NAME', 'CITY', 'TIME']
    for obj in read_request(request):
        field_names.append('defuziffy '+ obj)

    table.field_names = field_names

    for row in cursor.execute(sqlRequst):
        rowElements = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]
        for obj in read_request(request):
            rowElements.append(round(fuzzyMethods.defineFuzzify(obj, row[3], row[4], row[1], row[8]), 4))
        table.add_row(rowElements)

    #fuzzy_object_filtered.append(FUZZY_OBJECT(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    
    with open('table.txt', 'w') as w:
        w.write(str(table))

    with open('table.csv', 'w') as x:
        w = csv.writer(x)
        w.writerows(pretty_table_to_tuples(str(table)))
    database.close()
    
    for csvfile in glob.glob(os.path.join('.', '*.csv')):
        workbook = Workbook(csvfile[:-4] + '.xlsx')
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()

if __name__ == '__main__':
    main()

# for voltage in cursor:
#usefull loop
# sql = "SELECT ID,STATION_ID,VOLTAGE,CURRENT,TEMPERATURE,HUMIDITY,datetime(DATE,'localtime') as DATE FROM DANE WHERE STATION_ID = "+str(station) + " ORDER BY " + orderby;