from collections import deque

class Node:
    def __init__(self):
        self.parent = self
        self.size = 1
    def find(self):
        if self.parent == self:
            return self
        self.parent = self.parent.find()
        return self.parent
    def union(self,other):
        pa = self.find()
        pb = other.find()
        
        if pa == pb:
            return False
        
        if pa.size > pb.size:
            pa,pb = pb,pa
            
        pa.parent = pb
        pb.size += pa.size
        return True
        

def power_grid(w, h, s):
    N = len(s)
    
    assert w*h < 70000
    assert len(s) < 10000
    
    grid = [[None for _ in range(h)] for _ in range(w)]
    nodes = [Node() for _ in range(N)]
    
    edges = dict()

    qu = deque()
    for index,(x,y) in enumerate(s):
        grid[x][y] = index
        qu.append((index,x,y))
    
    while len(qu):
        index,x,y = qu.popleft()
        if x > 0:
            if grid[x-1][y] == None:
                grid[x-1][y] = index
                qu.append((index,x-1,y))
            elif index < grid[x-1][y]:
                other = grid[x-1][y]
                dist = abs(s[index][0]-s[other][0])+abs(s[index][1]-s[other][1])
                edges[(index, other)] = dist
        if y > 0:
            if grid[x][y-1] == None:
                grid[x][y-1] = index
                qu.append((index,x,y-1))
            elif index < grid[x][y-1]:
                other = grid[x][y-1]
                dist = abs(s[index][0]-s[other][0])+abs(s[index][1]-s[other][1])
                edges[(index, other)] = dist
        if x+1 < w:
            if grid[x+1][y] == None:
                grid[x+1][y] = index
                qu.append((index,x+1,y))
            elif index < grid[x+1][y]:
                other = grid[x+1][y]
                dist = abs(s[index][0]-s[other][0])+abs(s[index][1]-s[other][1])
                edges[(index, other)] = dist
        if y+1 < h:
            if grid[x][y+1] == None:
                grid[x][y+1] = index
                qu.append((index,x,y+1))
            elif index < grid[x][y+1]:
                other = grid[x][y+1]
                dist = abs(s[index][0]-s[other][0])+abs(s[index][1]-s[other][1])
                edges[(index, other)] = dist

    edges = [(d,x,y) for (x,y),d in edges.items()]
    edges.sort()
    dist = 0

    for d,i,j in edges:
        if nodes[i].union(nodes[j]):
            dist += d
            N -= 1
            if N == 1:
                break

    return dist
    
# Sett 'highscore' til True hvis du vil vises på poengtavlen.
# For mer info se 'https://algdat.idi.ntnu.no/ovinger.html#poengtavle'
# Merk: Kjøring for poengtavlen tar betraktelig lengre tid.
highscore = True

print(power_grid(4, 3, [(0,1), (0,2), (1,2), (2,1), (3,2), (3,0), (2,2)]))
print(power_grid(4, 3, [(0,1), (0,2), (1,2), (2,1), (3,2), (3,0)]))
