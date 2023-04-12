import math

import socket
import json

# Server information
SERVER_ADDRESS = ('192.168.43.234',2222)
BUFFER_SIZE = 1024
UDP_CLIENT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Directions():

    def __init__(self):
        self.dir = None
        self.x = None
        self.y = None
        self.p = None
        self.thickness = None

        self.data = []
    
    """Obtain the distance based on the number of pixels from
    current node to the farthest node based on the direction"""
    def _get_distance(self, line):
        x, y, h, w = line
        if self.dir == 0:
            distance = abs(self.x - x) / ( 38 * 2.54)
        elif self.dir == 1:
            distance = abs(self.x - (x+h)) / ( 38 * 2.54)
        elif self.dir == 2:
            distance = abs(self.y - y) / ( 38 * 2.54)
        elif self.dir == 3:
            distance = abs(self.y - (y+w)) / ( 38 * 2.54)

        return distance
    
    """Obtain the array of the bottom most coordinates, this will
    serve as the starting point to traverse the image"""
    def _get_bottom_most(self, array):
        if not array:
            return None

        bottom_most = array[0]
        for arr in array:
                if arr[0] + arr[2] > bottom_most[0] + bottom_most[2]:
                    bottom_most = arr
        
        array.pop(array.index(bottom_most))

        return bottom_most
    
    """Obtain the nearest line array from the current (x,y) location.
    Additionally, the nearest line will be removed from the array list
    to prevent future interactions"""
    def _get_near_line(self, array):
        min_dist = float("inf")
        nearest_line = None

        for line in array:
            x1, y1, h, w = line
            x2, y2 = x1 + h, y1 + w
            distances = [math.sqrt((self.x-x1)**2 + (self.y-y1)**2),
                         math.sqrt((self.x-x2)**2 + (self.y-y1)**2),
                         math.sqrt((self.x-x1)**2 + (self.y-y2)**2),
                         math.sqrt((self.x-x2)**2 + (self.y-y2)**2)]
            
            dist = min(distances)

            if dist < min_dist:
                min_dist = dist
                nearest_line = line

        array.remove(nearest_line)
        return nearest_line

    """Obtain the direction based on the current x and y to the
    next set of x and y for the line being traversed"""
    def _get_direction(self, array):
        x, y, h, w = array

        if self.x is None:
            if h > w:
                return 0
            else:
                return 3

        if h > w:
            if x < self.x:
                return 0
            elif self.x < x:
                return 1
        elif w > h:
            if y < self.y:
                return 2
            elif self.y < y:
                return 3
        
    """Main function - Binary image is passed to obtain a starting coordinate and direction
    Distance is calculated and returned alongside direction.
    Will only operate for 1 segment of the line until called again"""
    def _comm_command(self, array): 
        while True:
            if self.x is None:
                line = self._get_bottom_most(array)
                self.dir = self._get_direction(line)
                if self.dir == 0:
                    self.x = line[0] + line[2]
                    self.y = line[1]
                elif self.dir == 3:
                    self.x = line[0] + line[2]
                    self.y = line[1]
            else:
                line = self._get_near_line(array)
                prev_dir = self.dir
                self.dir = self._get_direction(line)

                if self.dir == 0 and prev_dir == 2:
                    self.x = line[0] + line[2]
                    self.y = line[1] + line[3]
                elif self.dir == 0 and prev_dir == 3:
                    self.x = line[0] + line[2]
                    self.y = line[1]

                elif self.dir == 1 and prev_dir == 2:
                    self.x = line[0]
                    self.y = line[1] + line[3]
                elif self.dir == 1 and prev_dir == 3:
                    self.x = line[0]
                    self.y = line[1]
                
                elif self.dir == 2 and prev_dir == 0:
                    self.x = line[0] + line[2]
                    self.y = line[1] + line[3]
                elif self.dir == 2 and prev_dir == 1:
                    self.x = line[0]
                    self.y = line[1] + line[3]

                elif self.dir == 3 and prev_dir == 0:
                    self.x = line[0] + line[2]
                    self.y = line[1]  
                elif self.dir == 3 and prev_dir == 1:
                    self.x = line[0]
                    self.y = line[1]           

            if self.dir != None:
                distance = round(self._get_distance(line),2)

                print("Distance: " + str(distance))
                print("Direction: " + str(self.dir))

                self.data.append([distance, self.dir])

                if self.dir == 0:
                    self.x = line[0]
                elif self.dir == 1:
                    self.x = line[0] + line[2]
                elif self.dir == 2:
                    self.y = line[1]
                elif self.dir == 3:
                    self.y = line[1] + line[3]
            if not array:
                break

        json_data = json.dumps(self.data)   
        UDP_CLIENT.sendto(json_data.encode(), SERVER_ADDRESS)

        self.data = []