# -*- coding: utf-8 -*-
import datetime
import serial  # http://pyserial.readthedocs.io/en/latest/pyserial.html
import time
from time import sleep
from threading import Thread
import os
import subprocess
import socket

# This code was adapted from rtek1000's code to reflect a NEO 6m GPS 
# Sensor wired to the GPIO pins
# Origional code can be found at:
# https://www.raspberrypi.org/forums/viewtopic.php?t=168440



#see http://www.gpsinformation.org/dale/nmea.htm#nmea

# Below is the origonal device defintion
# DEVICE = '/dev/ttyUSB0'
# Changed to'/dev/ttyAMA0' to represent sensor plugged into GPIO pins
DEVICE = '/dev/ttyAMA0'

DataBytes = ""
GpsUpdateInterval = 15  # minute
showGpsData = True
showUpdateMessage = True


def GpsDateTimeUpdate():
    global portRpi
    global DataBytes
    global showGpsData
    global showUpdateMessage
    global GpsUpdateInterval
    countTime = GpsUpdateInterval
    minuteOld = 0
    updateEnable = False
    while True:
        minuteNow = time.strftime("%M")
        if minuteOld != minuteNow:
            minuteOld = minuteNow
            countTime += 1
        if countTime > GpsUpdateInterval:
            countTime = 0
            updateEnable = True
            portRpi.reset_input_buffer()
        if updateEnable:
            if portRpi.isOpen():
                DataBytes = DataBytes + portRpi.read()
                if chr(13) in DataBytes:
                    if chr(10) in DataBytes:
                        DataBytes = DataBytes.replace(chr(10), "")
                    if chr(13) in DataBytes:
                        DataBytes = DataBytes.replace(chr(13), "")
                    list1 = DataBytes.split(',')
                    if (len(list1) == 13):
                        if((list1[0] == "$GPRMC") &
                        (len(list1[1]) == 9) &
                        (len(list1[9]) == 6)):
                            if(showGpsData):
                                print DataBytes
                                print
                            checksum = 0
                            for char in range(DataBytes.index('$') + 1,
                            DataBytes.index('*')):
                                checksum = (checksum ^ ord(DataBytes[char]))
                            list2 = list1[len(list1) - 1].split('*')
                            if len(list2) == 2:
                                if int(list2[1], 16) == checksum:
                                    hourGPS = int(list1[1][:2])
                                    minuteGPS = int(list1[1][2:4])
                                    secondGPS = int(list1[1][4:6])
                                    dayGPS = int(list1[9][:2])
                                    monthGPS = int(list1[9][2:4])
                                    yearGPS = int(list1[9][4:6])
                                    setDateTimeUTC(yearGPS,
                                                   monthGPS,
                                                   dayGPS,
                                                   hourGPS,
                                                   minuteGPS,
                                                   secondGPS)
                                    updateEnable = False
                                    minuteNow = time.strftime("%M")
                                    minuteOld = minuteNow
                                    if showUpdateMessage:
                                        print 'GPS update now'
                                        if(list1[2] == "A"):
                                            print 'Satellite mode'
                                        else:
                                            print 'Local RTC mode'
                                        print
                    DataBytes = ""
        else:
            sleep(0.1)


def setDateTimeUTC2(seconds_epoch):
    command_wait('date -u -s "@' + str(seconds_epoch) + '"')


def setDateTimeUTC(year, month, day, hour, minute, second):
    strUTCyear2set = str(year)
    strUTCmonth2set = str(month)
    strUTCday2set = str(day)
    strUTChour2set = str(hour)
    strUTCminute2set = str(minute)
    strUTCsecond2set = str(second)

    if(len(strUTCyear2set) < 4):
        strUTCyear2set = str(year + 2000)

    if(len(strUTCmonth2set) < 2):
        strUTCmonth2set = '0' + strUTCmonth2set

    if(len(strUTCday2set) < 2):
        strUTCday2set = '0' + strUTCday2set

    if(len(strUTChour2set) < 2):
        strUTChour2set = '0' + strUTChour2set

    if(len(strUTCminute2set) < 2):
        strUTCminute2set = '0' + strUTCminute2set

    if(len(strUTCsecond2set) < 2):
        strUTCsecond2set = '0' + strUTCsecond2set

    command_wait('date -u +%Y%m%d -s "' + strUTCyear2set +
                                          strUTCmonth2set +
                                          strUTCday2set + '"')

    command_wait('date -u +%T -s "' + strUTChour2set + ':' +
                                      strUTCminute2set + ':' +
                                      strUTCsecond2set + '"')

    seconds_epoch = time.mktime(datetime.datetime.now().timetuple())
    seconds_epoch += 3
    setDateTimeUTC2(seconds_epoch)


def command_wait(command):
    ## command = "sudo mount /dev/sda1 /mnt/usb"
    process = subprocess.Popen(command,
                               shell=True,
                               stdout=subprocess.PIPE)
    process.wait()
    if(process.returncode != 0):
        print 'command wait - error: '
        print process.returncode


def command_nowait(command):
    ## command = "sudo mount /dev/sda1 /mnt/usb"
    #process = subprocess.Popen(command,
    #                            shell=True,
    #                            stdout=subprocess.PIPE)
    subprocess.Popen(command,
                     shell=True,
                     stdout=subprocess.PIPE)
    ## process.wait()
    ## print process.returncode


def MyIP():
    print("IP: " + get_ip())


def get_ip():
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
    #command_wait("echo " + IP + " > /tmp/relogio.log")


if __name__ == '__main__':
    print 'Start update system DateTime from GPS'

    MyIP()

    print 'UTC: ' + str(datetime.datetime.utcnow())
    print 'Local: ' + str(datetime.datetime.now())

    print 'Test --> set UTC DateTime: 2016/01/01 12:00:00'
    setDateTimeUTC(2016, 1, 1, 12, 0, 0)

    if os.path.exists(DEVICE):
        try:
            portRpi = serial.Serial(DEVICE,
                                    timeout=None,
                                    baudrate=9600,
                                    xonxoff=False,
                                    rtscts=False,
                                    dsrdtr=False)
        except ValueError:
            print('Error: Serial Port')

    Thread1 = Thread(target=GpsDateTimeUpdate)
    Thread1.start()

    secondOld = 0

    while True:
        try:
            secondNow = time.strftime("%S")
            if secondOld != secondNow:
                secondOld = secondNow
                print 'UTC: ' + str(datetime.datetime.utcnow())
                print 'Local: ' + str(datetime.datetime.now())
                print
            sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            command_nowait("killall -9 python")

