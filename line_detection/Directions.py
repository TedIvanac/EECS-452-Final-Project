import numpy as np

class Directions():

    def __init__(self):
        self.dir = None
        self.x = None
        self.y = None
        self.p = None

    # Obtain the distance based on the number of pixels from
    # current node to the farthest node based on the direction
    def _get_distance(self):
        distance = abs(self.p) / ( 38 * 2.54)
        return distance
    
    # Obtain the x and y coordinate for the starting location
    def _get_x_y(self, diff):
        rows, cols = np.where(diff == 255)
        
        if rows.size == 0 or cols.size == 0:
            return None, None
        else:
            idx = np.argmax(rows)
            return rows[idx],cols[idx]

    # Obtain the lengths from current node to farthest nodes
    # in all directions. Based on greatest distance, a direction
    # is generated and returned alongside the greatest distance.
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
        max_dir_index = directions.index(max(directions))

        return directions[max_dir_index], max_dir_index

    # Obtain the starting coordinates and direction to traverse.
    # Otherwise change location to represent the distance travelled.
    # Additionally update adjacent node from travelled direction to 0.
    def _get_direction(self, diff):
        if self.x is None:
            self.x, self.y = self._get_x_y(diff)
            self.p, self.dir = self._get_h_w(diff)
        else:
            if self.dir == 0:
                self.x = self.x - self.p
                if self.x+1 < diff.shape[0]:
                    diff[self.x+1,self.y] = 0
            elif self.dir == 1:
                self.x = self.x + self.p
                if self.x-1 < 0:
                    diff[self.x-1,self.y] = 0
            elif self.dir == 2:
                self.y = self.y - self.p
                if self.y+1 < diff.shape[1]:
                    diff[self.x,self.y+1] = 0
            elif self.dir == 3:
                self.y = self.y + self.p
                if self.y-1 < 0:
                    diff[self.x,self.y-1] = 0

            self.p, self.dir = self._get_h_w(diff)

        return self.x, self.y, self.dir

    # Main function - Binary image is passed to obtain a starting coordinate and direction
    # Distance is calculated and returned alongside direction.
    # Will only operate for 1 segment of the line until called again
    def _comm_command(self, diff): 
        self.x, self.y, self.dir = self._get_direction(diff)

        if self.dir != None:
            distance = round(self._get_distance(),2)

            print("Distance: " + str(distance))
            print("Direction: " + str(self.dir))

            return distance, self.dir
            
        return None, None