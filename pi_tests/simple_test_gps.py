#!/usr/bin/env python3
# Based on the gps_simpletest.py example
# from https://github.com/adafruit/Adafruit_CircuitPython_GPS
# that was published by Adafruit.

# Imports all the libraries we use
import time
import board
import busio
import adafruit_gps
import csv

# Sets up the I2C interface for us to use
i2c = board.I2C()
# Create a GPS module instance using the I2C interface
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)

# Initialize the GPS module by changing what data it sends and at what rate.
# Turns on the basic GGA and RMC information streams
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Below are some other commands from the origional
# Adafruit code that you can uncomment for 
# different sets of data streams, depending
# on what you need.

# Turn on just minimum info (RMC only, location):
# gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn off everything:
# gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Tuen on everything (not all of it is parsed!)
# gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b"PMTK220,1000")


# Main loop runs forever printing the information you
# want constantly, about once a second
last_print = time.monotonic()

# Set up .csv file to log data to
csvfile = "gps_data.csv"
path = csv.reader(csvfile)
header = ['Latitude', 'Longitude', 'Fix Timestamp (UTC)']
with open(csvfile, "a") as fp:
    wr = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    wr.writerow(header)



# Try loop that allows for a graceful exit if needed
try:
    while True:

        gps.update()
        # Every second print out current location details if there's a fix.
        current = time.monotonic()
        if current - last_print >= 1.0:
            last_print = current
            if not gps.has_fix:
                # Try again if we don't have a fix yet.
                print("Waiting for fix...")
                continue
            # We have a fix! (gps.has_fix is true)
            # Print out details about the fix like location, date, etc.
            print("=" * 40)  # Print a separator line.
            fix_timestamp = " {}/{}/{} {:02}:{:02}:{:02}".format(
                    gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                    gps.timestamp_utc.tm_mday,  # struct_time object that holds
                    gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                    gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                    gps.timestamp_utc.tm_min,  # month!
                    gps.timestamp_utc.tm_sec,
                )
            print("Fix timestamp (UTC):", fix_timestamp)
            print("Latitude: {0:.6f} degrees".format(gps.latitude))
            print("Longitude: {0:.6f} degrees".format(gps.longitude))
            print("Fix quality: {}".format(gps.fix_quality))
            # Some attributes beyond latitude, longitude and timestamp are optional
            # and might not be present.  Check if they're None before trying to use!
            if gps.satellites is not None:
                print("# satellites: {}".format(gps.satellites))
            if gps.altitude_m is not None:
                print("Altitude: {} meters".format(gps.altitude_m))
            if gps.speed_knots is not None:
                print("Speed: {} knots".format(gps.speed_knots))
            if gps.track_angle_deg is not None:
                print("Track angle: {} degrees".format(gps.track_angle_deg))
            if gps.horizontal_dilution is not None:
                print("Horizontal dilution: {}".format(gps.horizontal_dilution))
            if gps.height_geoid is not None:
                print("Height geo ID: {} meters".format(gps.height_geoid))
    
            # Writes GPS data to the .csv file we set up before
            with open(csvfile, "a") as fp:
                wr = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                wr.writerow([gps.latitude, gps.longitude, fix_timestamp])

# Graceful exit
except (KeyboardInterrupt, SystemExit):
    print("\nExiting.")
    exit