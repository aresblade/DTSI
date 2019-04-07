import datetime
import time
import sqlite3
import unidecode
import itertools

fuzzy_values = ["low", "medium", "high", "critical"]
fuzzy_var_inputs = ["temperature", "voltage", "humidity"]

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

    database = sqlite3.connect('./jamedia.db')
    cursor = database.cursor()
    sql = "SELECT VOLTAGE FROM DANE"
    cursor.execute(sql)

    request = input('Write request: ')
    read_request(request)

    database.close()

if __name__ == '__main__':
    main()

# for voltage in cursor:
#usefull loop
# sql = "SELECT ID,STATION_ID,VOLTAGE,CURRENT,TEMPERATURE,HUMIDITY,datetime(DATE,'localtime') as DATE FROM DANE WHERE STATION_ID = "+str(station) + " ORDER BY " + orderby;