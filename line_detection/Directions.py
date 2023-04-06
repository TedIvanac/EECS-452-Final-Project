import numpy as np

class Directions():

    def __init__(self):
        self.dir = None
        self.x = None
        self.y = None
        self.p = None

    def _get_distance(self):
        distance = abs(self.p) / ( 38 * 2.54)
        # distance = (abs(end_x - start_x) + 1) * (abs(end_y - start_y) + 1) / (38 * 2.54)
        return distance
    
    def _get_x_y(self, diff):
        rows, cols = np.where(diff == 255)
        
        if rows.size == 0 or cols.size == 0:
            return None, None

        if self.dir is None:
            idx = np.argmax(rows)
            return rows[idx],cols[idx]
        elif self.dir == 0:
            idx = np.argmin(rows)
            return rows[idx],cols[idx]
        elif self.dir == 1:
            idx = np.argmax(cols)
            return rows[idx],cols[idx]
        elif self.dir == 2:
            idx = np.argmin(cols)
            return rows[idx],cols[idx]
        elif self.dir == 3:
            idx = np.argmax(rows)
            return rows[idx],cols[idx]

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

    def _comm_command(self, diff): 
        self.x, self.y, self.dir = self._get_direction(diff)
        
        if self.dir != None:
            distance = round(self._get_distance(),2)

            print("Distance: " + str(distance))
            print("Direction: " + str(self.dir))

            return str(distance), str(self.dir)
            
        return None, None