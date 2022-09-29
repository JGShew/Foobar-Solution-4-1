# This program uses the Edmonds-Karp algorithm for solving maximum flow problems.
# Details of the actual problem can be found https://stackoverflow.com/questions/61992364/escape-pods-google-foobar-challenge-max-flow-problem

capacities = []
currflows = []

def build_currflows():
    global capacities, currflows
    lencapacities = len(capacities)
    for i in range(lencapacities):
        row = []
        for j in range(lencapacities):
            row.append(0)
        currflows.append(row)
        

def adjust_flow(a, b, val):
    global currflows
    (currflows[a])[b] += val
    (currflows[b])[a] -= val

def remaining_flow(a, b):
    global capacities, currflows
    return (capacities[a])[b] - (currflows[a])[b]

def adjust_augpath(path):
    global capacities, currflows
    bottleneck = remaining_flow(path[0], path[1])
    for i in range(1, len(path) - 1):
        bottleneck = min(bottleneck, remaining_flow(path[i], path[i+1]))
    for i in range(0, len(path) - 1):
        adjust_flow(path[i], path[i+1], bottleneck)

def augpath(source, sink):
    global capacities
    bfsqueue = [[source]]
    nodesvisited = []
    currlevel = 0
    deadend = False
    sinkfound = False

    while sinkfound == False and deadend == False:
        deadend = True
        nextlevel = []
        for node in bfsqueue[currlevel]:
            for i in range(len(capacities[node])):
                if remaining_flow(node, i) > 0 and (i in nodesvisited) == False:
                    nextlevel.append(i)
                    nodesvisited.append(i)
                    deadend = False
                    if i == sink:
                        sinkfound = True
        bfsqueue.append(nextlevel)
        currlevel += 1
    
    if deadend == True:
        return []
    
    path = [sink]
    for i in range(-2, -1 - len(bfsqueue), -1):
        for node in bfsqueue[i]:
            if remaining_flow(node, path[0]) > 0:
                path.insert(0, node)
                break
    return path

def solution(entrances, exits, path):
    global capacities, currflows
    capacities = path
    build_currflows()

    for source in entrances:
        for sink in exits:
            augmentingpath = augpath(source, sink)
            while len(augmentingpath) > 0:
                adjust_augpath(augmentingpath)
                augmentingpath = augpath(source, sink)
    
    maxflow = 0
    for i in range(len(currflows)):
        for j in exits:
            maxflow += (currflows[i])[j]
    
    return maxflow