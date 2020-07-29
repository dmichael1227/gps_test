# Imports all the libraries we use
import serial
import time
import string
import pynmea2




# Try loop that allows for a graceful exit if needed
try:

    while True:
    	    # Sets the address of the NEO 6M GPS Sensor and delcares 
    	    # variables for simplification later on
    	    port="/dev/ttyAMA0"
	    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	    dataout = pynmea2.NMEAStreamReader()
	    newdata=ser.readline()

	    if newdata[0:6] == "$GPRMC":
		    newmsg=pynmea2.parse(newdata) # Reads the sensor data
		    lat = newmsg.latitude # Reads the data, assigns the Latitude to a variable
		    long = newmsg.longitude # Reads the data, assigns the Longitude to a variable
                    time = newmsg.timestamp # Reads the data, assigns the timestamp to a variable
		    gps = "Latitude= " + str(lat) + " and Longitude= " + str(long) # Sets this string as a variable, gps
		    print(gps) # Prints out the above string
                    












# Graceful exit
except (KeyboardInterrupt, SystemExit):
    print "\nExiting."
    exit
