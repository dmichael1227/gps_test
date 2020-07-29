#!/bin/sh
# launcher.sh


# run some commands that make sure the GPS sensor can actually read the data

sudo systemctl stop serial-getty@ttyAMA0.service
sudo systemctl disable serial-getty@ttyAMA0.service


# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/pi_tests
#sudo python gps_data_logger.py
cd /

