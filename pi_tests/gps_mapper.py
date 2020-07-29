# Imports all the libraries we use
import folium
import pandas as pd
import os
import webbrowser




# Sets up the colour scheme of the map
def colourgrad(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    g = int(max(0, 255*(ratio - 1)))
    r = 255 - b - g
    hexcolour = '#%02x%02x%02x' % (r,g,b)
    return hexcolour

# Reads the .csv file and assigns it to a variable
path = pd.read_csv('gps_mapping_data.csv')

# Uncomment these to have the values of the Latitude and Longitude columns printed out
#print (path["Latitude"])
#print (path["Longitude"])


# Sets up the map, writes the map parameters to a variable
mapPATH = folium.Map(location=[41.519917,-71.29445]) #,zoom_start=1000)
# Delete the ) , space, and # in front of #,zoom_start=1000) to 
# define a starting zoom

# Creates the map
for index, row in path.iterrows():
    lat = row["Latitude"]
    lng = row["Longitude"]
    folium.Marker([lat,lng]).add_to(mapPATH)

# Saves the map and opens it in a new tab of the webb rowser
mapPATH.save(outfile='RobotPath.html')
CWD = os.getcwd()
webbrowser.open_new('file://'+CWD+'/'+'RobotPath.html')
