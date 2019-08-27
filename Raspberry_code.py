#!/usr/bin/python3
from flask import Flask, render_template    
import serial  # to capture serial data from arduino
import time  # for pausing program in-between loop
import re  # for filtering strings from data list


port0 = "/dev/ttyACM0"  # Slow Blinker 
port1 = "/dev/ttyACM1"  # Fast Blinker 

ser0 = serial.Serial(port0, 9600, timeout =4)
ser1 = serial.Serial(port1, 9600, timeout =4)

start_dud = "b''"  # these duds are made when starting the program
blank_dud = ''


def readLine(ser):
    read_line = ser.read(ser.inWaiting())
    return read_line


def ignoreDud(line):
    dud_line = 'dud'
    if len(line) >= 40 and '(' not in line:
        return line
    else:
        return dud_line


def splitData(line):
    data_list = line.split(',')
    return data_list


def filterData(string):
    string = string.translate({ord(i): None for i in ' '})
    string = string.translate({ord(i): None for i in "brnABCDEFGHIJHLMNOPQRSTUVWXYZ:'\\"})
    if len(string) > 6:
        string = string[:6]
    else:
        pass
    return string    


def parseList(data_list):
    for i in range(len(data_list)):
        data_list[i] = filterData(data_list[i])
        try:
            data_list[i] = float(data_list[i])
        except ValueError:
            pass
        
    return data_list


def captureData(ser):
    line = readLine(ser)
    line = str(line)
    line = ignoreDud(line)
    if line != start_dud and line != blank_dud:
        data_list = splitData(line)
        data_list = parseList(data_list)
        return data_list
 

def removeOldCharacters(characterList):
    if len(characterList) > 3:
        del characterList[3:]
        return characterList
    else:
        return characterList
    
 

app = Flask(__name__)
@app.route('/')


def writeToServer():
    Arduino_zero_data = captureData(ser0)
    a0 = Arduino_zero_data
    removeOldCharacters(a0)
    
    Arduino_one_data = captureData(ser1)
    a1 = Arduino_one_data
    removeOldCharacters(a1)
    
    
    if a0 is not 'dud' and  not a1 is 'dud':
        try:
            smos0 = a0[0]
            ahum0 = a0[1]
            atemp0 = a0[2]
        
            smos1 = a1[0]
            ahum1 = a1[1]
            atemp1 = a1[2]
            
        except:
            smos0 = '-'
            ahum0 = '-'
            atemp0 = '-'
        
            smos1 = '-'
            ahum1 = '-'
            atemp1 = '-'

    templateData = {
        'title' : 'Greenhouse data',
        
        'zero_smos' : smos0,
        'zero_ahum' : ahum0,
        'zero_atemp' : atemp0,
        
        'one_smos' : smos1,
        'one_ahum' : ahum1,
        'one_atemp' : atemp1,
        }
    return render_template('index.html', **templateData)


while True:
    app.run(host='192.168.1.104', port=8080, debug=False)
    time.sleep(4)
