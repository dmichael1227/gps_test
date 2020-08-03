#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Revision $Id$

import rospy
import io

import pynmea2
import serial
from gps_comm.msg import GPS

def talker():
    pub = rospy.Publisher('gps', GPS, queue_size=10) #initialize publisher
    rospy.init_node('talker', anonymous=True) #initialize talker node
    rate = rospy.Rate(10) # 10hz
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5.0) #initialize serial object
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    lat=0.0
    lon=0.0
    while not rospy.is_shutdown():
        try:
            line = sio.readline() #read nmea sentence
            msg = pynmea2.parse(line)
            #print(repr(msg))
            if line.find('GGA') > 0: #search for GGA messages
                print("HIT")
                print(msg.latitude)
                print(msg.longitude)
                lat=float(msg.latitude) #convert to float
                lon=float(msg.longitude) #convert to float
        except serial.SerialException as e:
            print('Device error: {}'.format(e)) 
            continue
        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
            continue
        
        rospy.loginfo("Lat: %s Lon: %s",lat,lon) #log results
        pub.publish(lat,lon) #publish
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
