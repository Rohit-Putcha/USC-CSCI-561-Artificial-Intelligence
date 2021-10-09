from queue import PriorityQueue
import math

#A* Search Graph Traversal Algorithm
def Astar(graph, startNode, endNode):
        frontier = PriorityQueue()
        parent = {}
        pathCost = {}

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
                if child not in pathCost or neighborNodeCost < pathCost[child]:
                    parent[child] = currentNode
                    pathCost[child] = neighborNodeCost

                    #Priority is set to the child node cost and heuristic value from the child node
                    priority = neighborNodeCost + heuristic(child, endNode)
                    
                    #Check if child is not visited before and new child cost is lesser than existing path cost of that node
                    frontier.put((priority, child))

        return parent, pathCost

#Get Node Cost from previous node to present node
def getNodeCost(presentNode, previousNode):
        return 14 if sum(map(abs, [a - b for a, b in zip(presentNode, previousNode)])) == 2 else 10

#Calculate admissible heuristic from present node to end node
def heuristic(presentNode, endNode):
        return math.floor(math.sqrt(sum(map(lambda i: i * i, [a - b for a,b in zip(endNode, presentNode)]))))
