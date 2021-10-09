import FileReading 
import FileWriting
import BFS
import UCS
import Astar

inputCoordinates = FileReading.readInput('input.txt')
graph, algorithm, maxCoordinate, startCoordinate, endCoordinate = inputCoordinates

if algorithm == "BFS":
    optimalPathCostTuple = BFS.BFS(graph, startCoordinate, endCoordinate)
elif algorithm == "UCS":
    optimalPathCostTuple = UCS.UCS(graph, startCoordinate, endCoordinate)
elif algorithm == "A*":
    optimalPathCostTuple = Astar.Astar(graph, startCoordinate, endCoordinate)

FileWriting.writeOutput('output.txt', optimalPathCostTuple, startCoordinate, endCoordinate)