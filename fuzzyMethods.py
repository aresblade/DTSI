import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl

import datetime

class TIME_OBJECT:
    def __init__(self):
        self.morning = 'time > "3" and time < "11"'
        self.midday = 'time > "10" and time < "14"'
        self.afternoon = 'time > "11" and time < "18"'
        self.evening = 'time > "16" and time < "22"'
        self.night = 'time >= "0" and time < "5" and time > "20" and time <="24"'

class TEMPERATURE_OBJECT:
    def __init__(self):
        self.low = 'temperature < 20'
        self.medium = 'temperature > 15 and temperature < 30'
        self.high = 'temperature > 30'
        self.critical = 'temperature < 10 and temperature > 50'

class HUMIDITY_OBJECT:
    def __init__(self):
        self.low = 'humidity < 40'
        self.medium = 'humidity > 20 and humidity < 80'
        self.high = 'humidity > 60'

class VOLTAGE_OBJECT:
    def __init__(self):
        self.low = 'voltage < 11.5'
        self.medium = 'voltage > 11.5 and voltage < 13.5'
        self.high = 'voltage > 13'

def getSpecificTable(userArray):
    index = 0
    completeString = ''
    added = False
    for obj in userArray:
        if 'low temperature' in obj:
            completeString = completeString + ' ' + TEMPERATURE_OBJECT().low
            added = True
        elif 'medium temperature' in obj: 
            completeString = completeString + ' ' + TEMPERATURE_OBJECT().medium
            added = True 
        elif 'high temperature' in obj: 
            completeString = completeString + ' ' + TEMPERATURE_OBJECT().high
            added = True
        elif 'critical temperature' in obj: 
            completeString = completeString + ' ' + TEMPERATURE_OBJECT().critical
            added = True

        elif 'low humidity' in obj:
            completeString = completeString + ' ' + HUMIDITY_OBJECT().low
            added = True
        elif 'medium humidity' in obj: 
            completeString = completeString + ' ' + HUMIDITY_OBJECT().medium
            added = True
        elif 'high humidity' in obj: 
            completeString = completeString + ' ' + HUMIDITY_OBJECT().high
            added = True

        elif 'low voltage' in obj:
            completeString = completeString + ' ' + VOLTAGE_OBJECT().low
            added = True
        elif 'medium voltage' in obj: 
            completeString = completeString + ' ' + VOLTAGE_OBJECT().medium
            added = True

        elif 'high voltage' in obj: 
            completeString = completeString + ' ' + VOLTAGE_OBJECT().high
            added = True

        elif 'morning' in obj:
            completeString = completeString + ' ' + TIME_OBJECT().morning
            added = True

        elif 'midday' in obj: 
            completeString = completeString + ' ' + TIME_OBJECT().midday
            added = True

        elif 'afternoon' in obj: 
            completeString = completeString + ' ' + TIME_OBJECT().afternoon
            added = True

        elif 'evening' in obj: 
            completeString = completeString + ' ' + TIME_OBJECT().evening
            added = True

        elif 'night' in obj: 
            completeString = completeString + ' ' + TIME_OBJECT().night
            added = True
        else:
            added = False


        if index >= 0 and index < len(userArray) - 1 and added == True:
            completeString = completeString + ' and'

        index = index + 1

    while "and" in completeString[-3:len(completeString) + 1]:
        completeString = completeString[0:-3]

    return completeString

def defineFuzzify(obj, temperature, humidity, voltage, time): 
    if 'temperature' in obj:
        return temperatureFuzzify(obj, temperature)
    elif 'humidity' in obj:
        return humidityFuzzify(obj, humidity)
    elif 'voltage' in obj:
        return voltageFuzzify(obj, voltage)
    elif 'morning' in obj or 'midday' in obj or 'evening' in obj or 'night' in obj or 'afternoon' in obj :
        return timeFuzzify(obj, time)

def temperatureFuzzify(userArray, value):
    arrayValue = np.array([value])

    if 'low temperature' in userArray:
        if value <= 15:
            return 1
        elif value >= 20:
            return 0
        else:
            return fuzz.trimf(arrayValue, [15, 15, 20])[0]
    elif 'medium temperature' in userArray: 
        if value <= 15:
            return 0
        elif value >= 30:
            return 0
        else:
            return fuzz.trapmf(arrayValue, [15, 20, 25, 30])[0]
    elif 'high temperature' in userArray: 
        if value <= 35:
            return 0
        elif value >= 40:
            return 1
        else:
            return fuzz.trimf(arrayValue, [35, 40, 40])[0]
    elif 'critical temperature' in userArray: 
        if value <= 5:
            return 1
        elif value >= 55:
            return 1
        else:
            return abs(fuzz.trapmf(arrayValue, [5, 10, 50, 55])[0] - 1)

def humidityFuzzify(userArray, value):
    arrayValue = np.array([value])
 
    if 'low humidity' in userArray:
        if value <= 20:
            return 1
        elif value >= 30:
            return 0
        else:
            return fuzz.trimf(arrayValue, [20, 20, 30])[0]
    elif 'medium humidity' in userArray: 
        if value <= 20:
            return 0
        elif value >= 80:
            return 0
        else:
            return fuzz.trapmf(arrayValue, [20, 40, 60, 80])[0]
    elif 'high humidity' in userArray: 
        if value <= 70:
            return 0
        elif value >= 80:
            return 1
        else:
            return fuzz.trimf(arrayValue, [70, 80, 80])[0]

def voltageFuzzify(userArray, value):
    arrayValue = np.array([value])

    if 'low voltage' in userArray:
        if value <= 11.5:
            return 1
        elif value >= 12:
            return 0
        else:
            return fuzz.trimf(arrayValue, [11.5, 11.5, 12])[0]
    elif 'medium voltage' in userArray: 
        if value <= 11.5:
            return 0
        elif value >= 13.5:
            return 0
        else:
            return fuzz.trapmf(arrayValue, [11.5, 12, 13, 13.5])[0]
    elif 'high voltage' in userArray: 
        if value <= 13:
            return 0
        elif value >= 13.5:
            return 1
        else:
            return fuzz.trimf(arrayValue, [13, 13.5, 13.5])[0]

def timeFuzzify(userArray, value):
    value = datetime.datetime.strptime(value, '%H:%M:%S').hour + (datetime.datetime.strptime(value, '%H:%M:%S').minute / 60)
    arrayValue = np.array([value])

    if 'morning' in userArray:
        if value <= 3:
            return 0
        elif value >= 11:
            return 0
        else:
            return fuzz.trapmf(arrayValue, [3, 5, 9, 11])[0]
    elif 'midday' in userArray: 
        if value <= 10:
            return 0
        elif value >= 14:
            return 0
        else:
            return fuzz.trimf(arrayValue, [10, 12, 14])[0]
    elif 'afternoon' in userArray: 
        if value <= 11:
            return 0
        elif value >= 18:
            return 0
        else:
            return fuzz.trapmf(arrayValue, [11, 13, 16, 18])[0]
    elif 'evening' in userArray: 
        if value <= 16:
            return 0
        elif value >= 22:
            return 0
        else:
            return fuzz.trapmf(arrayValue, [16, 18, 20, 22])[0]
    elif 'night' in userArray: 
        if value <= 3:
            return 1
        elif value >= 22:
            return 1
        else:
            return abs(fuzz.trapmf(arrayValue, [3, 5, 20, 22])[0] - 1)

