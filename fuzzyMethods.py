import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl

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
    for obj in userArray:
        if index >= 1 and index < len(userArray):
            completeString = completeString + ' and'

        if 'low temperature' in obj:
            completeString = completeString + ' ' + TEMPERATURE_OBJECT().low
        elif 'medium temperature' in obj: 
            completeString = completeString + ' ' + TEMPERATURE_OBJECT().medium
        elif 'high temperature' in obj: 
            completeString = completeString + ' ' + TEMPERATURE_OBJECT().high
        elif 'critical temperature' in obj: 
            completeString = completeString + ' ' + TEMPERATURE_OBJECT().critical

        elif 'low humidity' in obj:
            completeString = completeString + ' ' + HUMIDITY_OBJECT().low
        elif 'medium humidity' in obj: 
            completeString = completeString + ' ' + HUMIDITY_OBJECT().medium
        elif 'high humidity' in obj: 
            completeString = completeString + ' ' + HUMIDITY_OBJECT().high

        elif 'low voltage' in obj:
            completeString = completeString + ' ' + VOLTAGE_OBJECT().low
        elif 'medium voltage' in obj: 
            completeString = completeString + ' ' + VOLTAGE_OBJECT().medium
        elif 'high voltage' in obj: 
            completeString = completeString + ' ' + VOLTAGE_OBJECT().high
        index = index + 1

    return completeString

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
            return fuzz.trapmf(arrayValue, [35, 40, 40])[0]
    elif 'critical temperature' in userArray: 
        if value <= 5:
            return 1
        elif value >= 55:
            return 1
        else:
            return abs(fuzz.trapmf(arrayValue, [5, 10, 50, 55])[0] - 1)
