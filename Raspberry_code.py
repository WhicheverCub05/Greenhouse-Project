import serial  # to capture serial data from arduino
import time  # for pausing program in-between loop
import re  # for filtering strings from data list

port = "/dev/ttyACM0"

ser = serial.Serial(port, 9600, timeout =2.1)


start_dud = "b''"  # these duds are made when starting the program
blank_dud = ''


def readLine(ser):
    read_line = ser.read(ser.inWaiting())
    return read_line


def ignoreDud(line):
    dud_line = ''
    if len(line) <= 50:
        return line
    else:
        return dud_line


def splitData(line):
    data_list = line.split(',')
    return data_list


def filterData(string):
    string = string.translate({ord(i): None for i in ' '})
    string = string.translate({ord(i): None for i in "brnABCDEFGHIJHLMNOPQRSTUVWXYZ:'\\"})
    return string    


def parseList(data_list):
    for i in range(len(data_list)):
        data_list[i] = filterData(data_list[i])
        try:
            data_list[i] = float(data_list[i])
        except ValueError:
            print('parsing error: string in data_list')
        
    return data_list


def captureData(ser):
    line = readLine(ser)
    line = str(line)
    line = ignoreDud(line)
    if line != start_dud and line != blank_dud:
        data_list = splitData(line)
        data_list = parseList(data_list)
        print(data_list)


while True:
    captureData(ser)
    time.sleep(2.1)


'''

testing the main sequence with one board

while True:
    start_dud = "b''"
    blank_dud = ''
    line = readLine(ser)
    line = str(line)
    line = ignoreDud(line)
    if line != start_dud and line != blank_dud:
        data_list = splitData(line)
        data_list = parseList(data_list)
        print(data_list)
    time.sleep(2.1)
'''

'''

this is just another method of filtering strings from integers
although, it does remove the bullet point from a string,
making a float into an integer which is not desirable.

def filterData(string):
    string = re.sub("[^0-9]", "", string)
    return string
 
''' 