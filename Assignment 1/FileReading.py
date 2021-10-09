from collections import defaultdict

#Function to read input
#Sample input file: 'input.txt'
def readInput(inputFileName):

    f = open(inputFileName, 'r+')

    graph = defaultdict(list)
    algorithm = str(f.readline().strip())
    maxCoordinates = tuple([int(i) for i in f.readline().split()])
    startCoordinate = tuple([int(i) for i in f.readline().split()])
    endCoordinate = tuple([int(i) for i in f.readline().split()])

    noOfGrids = int(f.readline())
    for i in range(noOfGrids):
        vertexWithOperation = [int(i) for i in f.readline().split()]
        parentNode = tuple(vertexWithOperation[0:3])
        operations = tuple(vertexWithOperation[3:])
        graph = addEdge(graph, parentNode, operations, maxCoordinates)

    f.close()

    return [graph, algorithm, maxCoordinates, startCoordinate, endCoordinate]

#Add Edges in adjacency list
def addEdge(graph, parentNode, operations, maxCoordinates):
    ops = {
        1: [1, 0, 0],
        2: [-1, 0, 0],
        3: [0, 1, 0],
        4: [0, -1, 0],
        5: [0, 0, 1],
        6: [0, 0, -1],
        7: [1, 1, 0],
        8: [1, -1, 0],
        9: [-1, 1, 0],
        10: [-1, -1, 0],
        11: [1, 0, 1],
        12: [1, 0, -1],
        13: [-1, 0, 1],
        14: [-1, 0, -1],
        15: [0, 1, 1],
        16: [0, 1, -1],
        17: [0, -1, 1],
        18: [0, -1, -1]
    }
    for i in operations:
        chosenOperation = ops.get(i)
        value = tuple([a + b for a, b in zip(parentNode, chosenOperation)])
        if (value[0] < maxCoordinates[0] and value[0] >= 0) and (value[1] < maxCoordinates[1] and value[1] >= 0) and (value[2] < maxCoordinates[2] and value[2] >= 0):
            graph[parentNode].append(value)

    return graph