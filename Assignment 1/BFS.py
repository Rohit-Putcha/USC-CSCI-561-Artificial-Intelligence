#Breadth First Search Graph Traversal Algorithm
def BFS(graph, startNode, endNode):
        frontier = []
        parent, pathCost = {}

        #Append startnode to frontier
        frontier.append(startNode)
        parent[startNode] = -1
        pathCost[startNode] = 0

        #Loop over frontier queue until it is empty
        while frontier:

            #Pop the First in element in the queue
            currentNode = frontier.pop(0)

            #Break loop when current node is end node
            if currentNode == endNode:
                break

            #Iterate over the adjacent nodes of current node in the graph
            for child in graph[currentNode]:
                neighborNodeCost = pathCost[currentNode] + 1

                #Check if child is not visited before
                if child not in pathCost:
                    parent[child] = currentNode
                    pathCost[child] = neighborNodeCost

                    #Append the child node to frontier
                    frontier.append(child)

        #Return parent array for optimal path and path cost array for optimal path cost 
        return parent, pathCost