import numpy as np

class Directions():

    def __init__(self):
        self.dir = None
        self.x = None
        self.y = None
        self.thickness = None

    def _get_distance(self,diff):

        if self.dir == 0:  # Up
            start_x, end_x, start_y, end_y = self.x, self.x, self.y, self.y
            while start_x > 0 and diff[start_x - 1, start_y] == 1: 
                diff[start_x, start_y] = 0
                start_x -= 1
            while end_x < diff.shape[0] - 1 and diff[end_x + 1, end_y] == 1: end_x += 1
        elif self.dir == 1:  # Down
            start_x, end_x, start_y, end_y = self.x, self.x, self.y, self.y
            while start_x < diff.shape[0] - 1 and diff[start_x + 1, start_y] == 1: 
                diff[start_x, start_y] = 0
                start_x += 1
            while end_x > 0 and diff[end_x - 1, end_y] == 1: end_x -= 1
        elif self.dir == 2:  # Left
            start_x, end_x, start_y, end_y = self.x, self.x, self.y, self.y
            while start_y > 0 and diff[start_x, start_y - 1] == 1: 
                diff[start_x, start_y] = 0
                start_y -= 1
            while end_y < diff.shape[1] - 1 and diff[end_x, end_y + 1] == 1: end_y += 1
        elif self.dir == 3:  # Right
            start_x, end_x, start_y, end_y = self.x, self.x, self.y, self.y
            while start_y < diff.shape[1] - 1 and diff[start_x, start_y + 1] == 1: 
                diff[start_x, start_y] = 0
                start_y += 1
            while end_y > 0 and diff[end_x, end_y - 1] == 1: end_y -= 1
        else:
            return 0

        self.x = start_x
        self.y = start_y
        distance = (abs(end_x - start_x) + 1) * (abs(end_y - start_y) + 1) / (38 * 2.54)

        return distance
    
    def _get_x_y(self, diff):
        rows, cols = np.where(diff == 1)
        
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

    def _get_thickness(self, diff):
        h_thickness = 0
        w_thickness = 0

        i = self.x
        while True:
            if diff[i,self.y] == 1:
                h_thickness += 1
                i -= 1
            if i < 0 or diff[i, self.y] == 0:
                break

        i = self.y
        while True:
            if diff[self.x, i] == 1:
                w_thickness += 1
                i += 1
            if i >= diff.shape[1] or diff[self.x, i] == 0:
                break

        return h_thickness, w_thickness

    def _get_direction(self, diff):
        self.dir = None
        if self.x is None:
            self.x, self.y = self._get_x_y(diff)
            h, w = self._get_thickness(diff)
    
        directions = [
            (-1, 0, 0),  # Up
            (0, 1, 3),   # Right
            (1, 0, 1),   # Down
            (0, -1, 2)   # Left
        ]

        for dx, dy, direction in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if new_x < 0 or new_x >= diff.shape[0] or new_y < 0 or new_y >= diff.shape[1]:
                continue
            if diff[new_x,new_y] == 1:
                self.dir = direction
                return self.x, self.y, direction
        self.dir = None
        return 0, 0, self.dir

    def _comm_command(self, diff): 
        self.x, self.y, self.dir = self._get_direction(diff)
        
        if self.dir != None:
            distance = self._get_distance(diff)

            print("Distance: " + str(distance))
            print("Direction: " + str(self.dir))

            return diff, distance, self.dir
            
        return diff, None, None