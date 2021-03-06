import sys
import numpy as np
from collections import defaultdict
import copy

def main(inputFile):
    #sys.setrecursionlimit(20)
    mapA = riskMap(inputFile)
    mapA.pathfinder((0,0), [])
    print(mapA.lowpath())
    

class riskMap:
    def __init__(self, mapFile):
        #read in as nested list, then throw into numpy array
        self.map = []
        with open(mapFile, 'r') as file:
            self.map = [list(map(int, line.rstrip("\n"))) for line in file]

        self.map = np.array(self.map)
        self.mapx, self.mapy = self.map.shape

        #fixed end point to bottom right.
        self.finish = (self.mapx-1,self.mapy-1)

        self.visited = set()
        self.paths = []

        self.counter = 0

    def pathfinder(self, origin, currentPath):
        self.visited.add(origin)
        newPath = copy.deepcopy(currentPath)
        newPath.append(origin)
#        print('path', newPath)

        x, y = origin
        #two step list comprehension for convenience
        rawNeighbours = [(x+dx, y+dy) for dx, dy in [(0, 1),  (-1, 0), (1, 0), (0, -1)]]
        neighbours = [neighbour for neighbour in rawNeighbours if not neighbour in newPath]

        neighbourdict = defaultdict(int)
        #get values of neighbours, but needs to be linked to coords...
        for x, y in neighbours:
            if 0 <= x < self.mapx and 0 <= y < self.mapy:
                neighbourdict[(x,y)]=self.map[x][y]

#        print('visited', self.visited)
        #print('neighbours', sorted(neighbourdict.items(), key=lambda x: x[1]))
        #go over all neighbours in ascending order of their value.
        for position, value in sorted(neighbourdict.items(), key=lambda x: x[1]):
            #print(position, value)
            if not position in newPath:
                self.visited.add(position)
                if position == self.finish:
                    print('hooray', len(newPath))
                    newPath.append(position)
                    self.paths.append(newPath)
                    print(newPath)
                    return
                else:
                    self.pathfinder(position, newPath)



        


    def lowpath(self):
        sums = []
        for path in self.paths:
            pathsum = 0
            for x, y in path:
                pathsum += self.map[x,y]

            sums.append(pathsum)

        return sums


if __name__ == "__main__":
    #only pass through the first argument which should be the inputfile
    main(sys.argv[1])