#Function to write output to file
#Sample output file: "output.txt"
def writeOutput(outputFileName, optimalPathCostTuple, startNode, endNode):
    parent = optimalPathCostTuple[0]
    pathCost = optimalPathCostTuple[1]
    optimalPath = []
    currentNode = endNode
    f = open(outputFileName, "w")

    #Output FAIL in case current node not present in parent array
    if currentNode not in parent:
        f.writelines("FAIL")
        f.close()
        return

    #Backtrack the parent array from end node to the start node, for the optimal path
    while(parent[currentNode] != -1):
        optimalPathNode = '{} {}'.format(' '.join(map(str, currentNode)), str(
            pathCost[currentNode] - pathCost[parent[currentNode]]))
        optimalPath.insert(0, optimalPathNode)
        currentNode = parent[currentNode]

    optimalPath.insert(0, '{} {}'.format(' '.join(map(str, startNode)), 0))
    outputText = [str(pathCost[endNode]), str(len(optimalPath))]
    outputText += optimalPath
    f.writelines("\n".join(outputText))
    f.close()