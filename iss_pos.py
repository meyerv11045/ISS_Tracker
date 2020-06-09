''' Vikram Meyer 5/5/20
    Uses an open-notify API to retrieve and display information about the ISS
'''
import json
import urllib.request
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from math import cos,sin
import time

def get_astronauts():
    ''' Calls to an API for the current astronauts in space
        Prints the names and craft of the astronauts
        Example API Response:
        {"number": 3, "message": "success", "people": [{"craft": "ISS", "name": "Chris Cassidy"}, 
        {"craft": "ISS", "name": "Anatoly Ivanishin"}, {"craft": "ISS", "name": "Ivan Vagner"}]}

    '''
    url = "http://api.open-notify.org/astros.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read()) #Putting the JSON response into a dictionary 
    print("{} People in Space: ".format(result["number"]))
    print("-------------------")
    people = result["people"]
    for i,p in enumerate(people):
        print("{}) {} on the {}".format(i+1,p["name"],p["craft"]))

def get_ISS_pos():
    ''' Calls to an API to get the current position of the ISS
        Returns a tuple of strings ('longitude','latitude')
        Example API Response: 
        {"message": "success", "iss_position": 
        {"longitude": "-152.6450", "latitude": "21.9032"}, "timestamp": 1588705974}
    '''
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    return tuple(result["iss_position"].values())

def get_time_of_passover(position):
    ''' Takes a tuple (longitude,latitude)
        Prints the next time the ISS is next visible
    '''
    
    def to_mins(secs):
        minutes = secs // 60
        sec_remaining = secs % 60
        return "{} minutes and {} seconds".format(minutes,sec_remaining) 

    url = "http://api.open-notify.org/iss-pass.json?lat={}&lon={}".format(position[1],position[0])
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    over = time.ctime(result["response"][1]["risetime"]) #Converts a time in sec to a string representing local time
    duration = result["response"][1]["duration"]
    print("{} for {}".format(over,to_mins(duration)))

def plot_earth(iss,pos1):
    ''' Takes iss and pos1 as tuples of strings ('longitude','latitude')
        Uses spherical to cartesian cordinates to plot the globe 
        Uses geodetic to cartesian cordinates to plot positions
    '''
    R = 6_371_000 #Radius of Earth in meters
    def sphere(r): 
        theta = np.linspace(0,2 * np.pi, 40)
        phi = np.linspace(0,np.pi,40)
        phi,theta = np.meshgrid(phi,theta)

        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        return (x,y,z)
    
    def geo_to_cartesian(cords):
        lon,lat = cords
        lon = float(lon)
        lat = float(lat)
        x = R * cos(lat) * cos(lon)
        y = R * cos(lat) * sin(lon)
        z = R * sin(lat)
        return (x,y,z)

    x_s,y_s,z_s = sphere(R)
    x_i,y_i,z_i = geo_to_cartesian(iss)
    x_h,y_h,z_h = geo_to_cartesian(pos1)

    _ = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(x_s,y_s,z_s)
    ax.scatter3D(x_i,y_i,z_i,s=50,color='red')
    ax.scatter3D(x_h,y_h,z_h,s=100,color='green')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

if __name__ =="__main__":
    cinci = (-84.51201,39.103119) #longitude,latitude
    equator = (-77.9885,0)
    get_time_of_passover(cinci)
    iss_cords = get_ISS_pos()
    plot_earth(iss_cords,equator)

''' Math Resources
    Spherical Coordinates:
    https://vvvv.org/blog/polar-spherical-and-geographic-coordinates
    http://tutorial.math.lamar.edu/Classes/CalcIII/SphericalCoords.aspx
    
    Geodetic to Cartesian Coordinates:
    http://www.movable-type.co.uk/scripts/latlong.html
    https://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates
    https://vvvv.org/blog/polar-spherical-and-geographic-coordinates
    https://www.linz.govt.nz/data/geodetic-system/coordinate-conversion/geodetic-datum-conversions/equations-used-datum
    https://www.e-education.psu.edu/geog862/book/export/html/1669
'''