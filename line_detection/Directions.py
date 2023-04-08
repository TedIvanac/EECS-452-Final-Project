import numpy as np
import math

import socket
import json

# Server information
SERVER_ADDRESS = ('192.168.0.23',2222)
BUFFER_SIZE = 1024
UDP_CLIENT = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Directions():

    def __init__(self):
        self.dir = None
        self.x = None
        self.y = None
        self.p = None

        self.data = []

    def _get_midpoint(self, prev):
        if self.dir in [0,1]:
            midpoint = math.ceil((self.x+prev)/2)
        elif self.dir in [2,3]:
            midpoint = math.ceil((self.y+prev)/2)

        return midpoint
    
    def _get_length(self, midpoint,diff):
        k = 0
        l = 0
        i = 0
        j = 0
        while True:
            if self.dir in [0,1]:
                # To the right of the midpoint
                if self.y + i < diff.shape[1] and diff[midpoint,self.y+i] == 1:
                    k += 1
                    i += 1
                # To the left of the midpoint
                if self.y - j >= 0 and diff[midpoint, self.y-j] == 1:
                    l += 1
                    j += 1
                # Break if both sides equal 0 
                if diff[midpoint, self.y+i] == 0 and diff[midpoint, self.y-j] == 0:
                    break

            elif self.dir in [2,3]:
                # To the bottom of the midpoint
                if self.x + i < diff.shape[0] and diff[self.x+i,midpoint] == 1:
                    k += 1
                    i += 1
                # To the top of the midpoint
                if self.y - j >= 0 and diff[self.x-j, midpoint] == 1:
                    l += 1
                    j += 1
                # Break if both sides equal 0
                if diff[self.x+i, midpoint] == 0 and diff[self.x-j,midpoint] == 0:
                    break

        return l, k



    """Obtain the distance based on the number of pixels from
    current node to the farthest node based on the direction"""
    def _get_distance(self):
        distance = abs(self.p) / ( 38 * 2.54)
        return distance
    
    """Obtain the x and y coordinate for the starting location"""
    def _get_x_y(self, diff):
        rows, cols = np.where(diff == 255)
        
        if rows.size == 0 or cols.size == 0:
            return None, None
        else:
            idx = np.argmax(rows)
            return rows[idx],cols[idx]

    """Obtain the lengths from current node to farthest nodes
    in all directions. Based on greatest distance, a direction
    is generated and returned alongside the greatest distance."""
    def _get_h_w(self, diff):
        h_up = 0
        w_right = 0
        h_down = 0
        w_left = 0

        i = self.x-1
        while True:
            if i < 0 or diff[i, self.y] == 0:
                break
            if diff[i,self.y] == 255:
                h_up += 1
                i -= 1

        i = self.y+1
        while True:
            if i >= diff.shape[1] or diff[self.x, i] == 0:
                break
            if diff[self.x, i] == 255:
                w_right += 1
                i += 1
            
        i = self.x+1
        while True:
            if i >= diff.shape[0] or diff[i, self.y] == 0:
                break
            if diff[i,self.y] == 255:
                h_down -= 1
                i += 1
            
        i = self.y-1
        while True:
            if i < 0 or diff[self.x, i] == 0:
                break
            if diff[self.x, i] == 255:
                w_left -= 1
                i -= 1
            
        directions = [h_up, abs(h_down), abs(w_left), w_right]

        if all(x == 0 for x in directions):
            return None, None

        max_dir_index = directions.index(max(directions))

        return directions[max_dir_index], max_dir_index

    """Obtain the starting coordinates and direction to traverse.
    Otherwise change location to represent the distance travelled.
    Additionally update adjacent node from travelled direction to 0."""
    def _get_direction(self, diff):
        # First iteration
        if self.x is None:
            self.x, self.y = self._get_x_y(diff)
            self.p, self.dir = self._get_h_w(diff)
        # Every iteration after the first
        else:
            if self.dir == 0:
                prev = self.x
                self.x = self.x - self.p
                mp = self._get_midpoint(prev)
                l, k = self._get_length(mp, diff)

                if self.x+1 < diff.shape[0]:
                    diff[prev:self.x+1:-1,self.y-l:self.y+k] = 0

            elif self.dir == 1:
                prev = self.x
                self.x = self.x + self.p
                mp = self._get_midpoint(prev)

                if self.x-1 < 0:
                    diff[prev:self.x-1,self.y-l:self.y+k] = 0

            elif self.dir == 2:
                prev = self.y
                self.y = self.y - self.p
                mp = self._get_midpoint(prev)

                if self.y+1 < diff.shape[1]:
                    diff[self.x-l:self.x+k,prev:self.y+1:-1] = 0

            elif self.dir == 3:
                prev = self.y
                self.y = self.y + self.p
                mp = self._get_midpoint(prev)

                if self.y-1 < 0:
                    diff[self.x-l:self.x+k,prev:self.y-1] = 0

            self.p, self.dir = self._get_h_w(diff)

        return self.x, self.y, self.dir

    """Main function - Binary image is passed to obtain a starting coordinate and direction
    Distance is calculated and returned alongside direction.
    Will only operate for 1 segment of the line until called again"""
    def _comm_command(self, diff): 
        while True:
            self.x, self.y, self.dir = self._get_direction(diff)
            
            if self.dir == None:
                break
            if self.dir != None:
                distance = round(self._get_distance(),2)

                print("Distance: " + str(distance))
                print("Direction: " + str(self.dir))

                self.data.append([distance, self.dir])

        json_data = json.dumps(self.data)   
        UDP_CLIENT.sendto(json_data.encode(), SERVER_ADDRESS)