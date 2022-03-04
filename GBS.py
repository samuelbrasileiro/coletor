class PriorityQueue(object):
    def __init__(self):
        self.queue = []
  
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
  
    # for checking if the queue is empty
    def empty(self):
        return len(self.queue) == 0
  
    # for inserting an element in the queue
    def put(self, priority, data):
        self.queue.append([priority, data])
  
    # for popping an element based on Priority
    def get(self):
        try:
            min = 0
            for i in range(0,len(self.queue)):
                if self.queue[i][0] < self.queue[min][0]:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            print()
            exit()  


class GBS():
    """
    Implements the BFS or DFS path finding algorithm
    """
    def __init__(self, map, pathViewer):
        self.parent = {}
        self.visited = set()
        self.container = PriorityQueue() # It is a Queue if BFS and a Stack if DFS

        self.map = map
        self.viewer = pathViewer
    
    def getNeighbours(self, rowPos, colPos):
        up = (rowPos - 1, colPos)
        down = (rowPos + 1, colPos)
        left = (rowPos, colPos - 1)
        right = (rowPos, colPos + 1)
        diag_up_right = (rowPos + 1, colPos + 1)
        diag_down_right = (rowPos - 1, colPos + 1)
        diag_up_left = (rowPos + 1, colPos - 1)
        diag_down_left = (rowPos - 1, colPos - 1)

        return [up, diag_up_right, right, diag_down_right, down, diag_down_left, left, diag_up_left]

    def isValidNeighbour(self, rowPos, colPos):
        # If tile is beyond the map
        if (rowPos < 0 or colPos < 0): return False
        if (rowPos >= self.map.rows or colPos >= self.map.columns): return False
        # Else: if tile is not blocked by an obstacle
        return not self.map.isTileBlocked(rowPos, colPos)
    
    def distance(self, pos1x, pos1y, pos2x, pos2y):
        return sqrt((pos1x - pos2x)**2 + (pos1y - pos2y)**2)
        
    def findPath(self, startPos, targetPos):
        # Define start and target tiles
        startRow, startCol = self.map.gridPositionFromPosition(startPos)
        targetRow, targetCol = self.map.gridPositionFromPosition(targetPos)
        target = (targetRow, targetCol)
        start = (startRow, startCol)
        
        # Step 1: put the start tile in the container
        self.container.put(self.distance(start[0],start[1],target[0],target[1]), start)
        self.parent[start] = None

        while not self.container.empty():
            # Step 2: take a tile of the container and add it to the visited list of tiles (if not already in there)
            current = self.container.get()[1]
            if current in self.visited:
                continue

            # Stop condition: if the popped item of the container corresponds to the target
            if current == target:
                return self.backtrace(start, target)

            (row, col) = current
            if current not in self.visited:
                row, col = current
                self.viewer.paintExploredNode(col, row)
                self.visited.add(current)
                self.map.visited.append(current)
            
            # Step 3: create a list of neighbour tiles and add the ones which aren't in the visited list to the top of the container
            neighbours = self.getNeighbours(row, col)
            for neighbour in neighbours:
                (neighbourRow, neighbourCol) = neighbour
                # If the neighbour wasn't visited and is valid
                if neighbour not in self.visited and self.isValidNeighbour(neighbourRow, neighbourCol):
                    cost = self.distance(target[0], target[1], neighbour[0], neighbour[1])
                    # Add to the top of the container
                    self.container.put(cost, neighbour)
                    if neighbour not in self.parent:
                        self.parent[neighbour] = current
        
        return []
         
    def backtrace(self, start, target):
        """
        Backtraces path from target to start
        """
        (startRow, startCol) = start
        (targetRow, targetCol) = target
        path = [(targetCol, targetRow)]

        current = target
        while self.parent[current] != None:
            (parentRow, parentCol) = self.parent[current]
            path.append((parentCol, parentRow))
            current = self.parent[current]
        
        # Paint path including the vehicle position
        path.append((startCol, startRow))
        path.reverse()
        self.viewer.paintPath(path)
        
        # Take out the vehicle position
        path.pop(0)
        return path