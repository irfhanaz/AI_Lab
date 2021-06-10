import copy
class Side:
    miss = 0
    cann = 0
    dict= {}
    def __init__(self, m = 0, c = 0): 
        self.miss = m
        self.cann = c
    def __add__(self, new): #returning
        self.miss += new.miss
        self.cann += new.cann
        return self
    def __sub__(self, new): #departing
        self.miss -= new.miss
        self.cann -= new.cann
        return self
    def Safe(self): #everyone survives?
        return (self.miss >= 0 and self.cann >= 0 and (self.miss == 0 or (self.miss >= self.cann)))
    def __str__(self): #prints the status after each move
        return ("[" + str(self.miss) + "M, " + str(self.cann) + "C]")
class State:
    depart = None
    arrive = None
    startSide = True
    prevMove = None
    def __init__(self, n = Side(), f = Side()): 
        self.depart = n
        self.arrive = f
    def cross(self, travelers):
        self.prevMove = travelers
        if self.startSide:
            self.depart -= travelers
            self.arrive += travelers
        else:
            self.depart += travelers
            self.arrive -= travelers
        self.startSide = not self.startSide
    def Safe(self):
        return self.depart.Safe() and self.arrive.Safe()
    def reachedTarget(self):
        return not self.startSide and (self.depart.miss == 0 and self.depart.cann == 0)
    def __str__(self):
        whichSide = lambda isNear: (isNear and ["S"] or ["F"])[0]
        safe = lambda Safe: (Safe and [""] or ["[i]"])[0]
        return "%s : %s%s | | %s%s" % (whichSide(self.startSide), self.depart, safe(self.depart.Safe()), self.arrive, safe(self.arrive.Safe()))
def main(m,c,p):
    q = [State(Side(m, c))]
    searched = {}
    while len(q) > 0: #BFS
        current = q[0]
        del q[0]
        if current.reachedTarget(): break
        searched[str(current)] = True
        for miss in range(0, p+1):
            for cann in range(max(0, 1 - miss), p+1 - miss):
                new = copy.deepcopy(current)
                new.parent = current
                new.cross(Side(miss, cann))
                transition = "%s + [%s M, %s C] --> %s (%d)" % (current, miss, cann, new, len(q))
                if ((not new.Safe()) or (str(new) in searched)):
                    pass
                else:
                    q.append(new)

    path = ""
    i=0
    while current is not None:
        path = " + %s\n %s %s" % (current.prevMove, current, path)
        try:
            current = current.parent
            i=i+1
        except AttributeError:
            current = None
    path = path[8:]
    print("Breadth-First Solution:")
    print(path)
    print("Successfully crossed the river with %s crossings." % str(i))
    print("\n\n")
if __name__=="__main__":
    main(3,3,2)
