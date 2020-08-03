#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from gps_comm.msg import GPS

def callback(data):
    rospy.loginfo('Lat: %s Lon %s', round(data.Lat,4),round(data.Lon,4))

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('gps', GPS, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
