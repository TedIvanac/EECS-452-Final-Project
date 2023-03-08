import numpy as np

class Directions():

    def __init__(self):
        self.dir = None

    def _get_distance(self, diff):
        # 38 pixels ~= 1 cm
        # 1 inch = 2.54 cm
        # Distane is in inches
        x, y = self._get_x_y(diff)

        if self.dir == 0:  # Up
            start_x, end_x, start_y, end_y = x, x, y, y
            while start_x > 0 and diff[start_x - 1, start_y] == 1: start_x -= 1
            while end_x < diff.shape[0] - 1 and diff[end_x + 1, end_y] == 1: end_x += 1
        elif self.dir == 1:  # Down
            start_x, end_x, start_y, end_y = x, x, y, y
            while start_x < diff.shape[0] - 1 and diff[start_x + 1, start_y] == 1: start_x += 1
            while end_x > 0 and diff[end_x - 1, end_y] == 1: end_x -= 1
        elif self.dir == 2:  # Left
            start_x, end_x, start_y, end_y = x, x, y, y
            while start_y > 0 and diff[start_x, start_y - 1] == 1: start_y -= 1
            while end_y < diff.shape[1] - 1 and diff[end_x, end_y + 1] == 1: end_y += 1
        elif self.dir == 3:  # Right
            start_x, end_x, start_y, end_y = x, x, y, y
            while start_y < diff.shape[1] - 1 and diff[start_x, start_y + 1] == 1: start_y += 1
            while end_y > 0 and diff[end_x, end_y - 1] == 1: end_y -= 1
        else:
            return 0

        distance = (abs(end_x - start_x) + 1) * (abs(end_y - start_y) + 1) * (38 * 2.54)

        return distance
    
    def _get_length(self, diff):
        rows, cols = np.where(diff == 1)
        if rows.size == 0 or cols.size == 0:
            return None, None
        
        h = np.max(rows) - np.min(rows)
        w = np.max(cols) - np.min(cols)

        return h, w

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

    def _check_approx(self,diff,x,y,orientation='h'):
        if orientation == 'h':
            if (diff[x-1,y] == 1):
                return 0 # forward
            elif (diff[x+1,y] == 1):
                return 1 # backward
        elif orientation == 'w':
            if (diff[x,y-1] == 1):   
                return 2 # left
            elif (diff[x,y+1] == 1):   
                return 3 # right   

    def _get_direction(self, diff):
        x, y = self._get_x_y(diff)
    
        directions = [
            (-1, 0, 0),  # Up
            (0, 1, 3),   # Right
            (1, 0, 1),   # Down
            (0, -1, 2)   # Left
        ]

        for dx, dy, direction in directions:
            new_x, new_y = x + dx, y + dy
            if new_x < 0 or new_x >= diff.shape[0] or new_y < 0 or new_y >= diff.shape[1]:
                continue
            if diff[new_x,new_y] == 1:
                self.dir = direction
                return self.dir

        self.dir = None
        return self.dir

    def _comm_command(self, diff):
                
        self.dir = self._get_direction(diff)
        
        if self.dir != None:
            distance = self._get_distance(diff)

            if self.dir == 0:
                print('Going forward: ' + str(distance) + ' inches')
            elif self.dir == 1:
                print('Turning around: ' + str(distance) + ' inches')
            elif self.dir == 2:
                print('Turning left: ' + str(distance) + ' inches')
            elif self.dir == 3:
                print('Turning right: ' + str(distance) + ' inches')