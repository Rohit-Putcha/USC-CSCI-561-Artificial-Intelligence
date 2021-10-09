from queue import PriorityQueue

#Uniform Cost Search Graph Traversal Algorithm
def UCS(graph, startNode, endNode):
        parent = {}
        pathCost = {}
        frontier = PriorityQueue()

        #Put startnode in frontier
        frontier.put((0, startNode))
        parent[startNode] = -1
        pathCost[startNode] = 0

        #Loop over frontier queue until it is empty
        while frontier.queue:

            #Pop the highest priority element from frontier
            priority, currentNode = frontier.get()
            
            #Break loop when current node is end node
            if currentNode == endNode:
                break

            #Iterate over the adjacent nodes of current node in the graph
            for child in graph[currentNode]:
                neighborNodeCost = pathCost[currentNode] + getNodeCost(child, currentNode)
                
                #Check if child is not visited before and new child cost is lesser than existing path cost of that node
                if child not in pathCost or neighborNodeCost < pathCost[child]:
                    parent[child] = currentNode
                    pathCost[child] = neighborNodeCost                    
                    priority = neighborNodeCost
                    
                    #Put the child node in frontier
                    frontier.put((priority, child))
                    
        return parent, pathCost

#Get Node Cost from previous node to present node
def getNodeCost(presentNode, previousNode):
        return 14 if sum(map(abs, [a - b for a, b in zip(presentNode, previousNode)])) == 2 else 10