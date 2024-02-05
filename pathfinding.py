### Package Imports ###
import heapq
import abc
from operator import truediv
from typing import List, Optional, Tuple


class Stack:
    """A container with a last-in-first-out (LIFO) queuing policy."""
    def __init__(self):
        self.list = []

    def push(self,item):
        """Push 'item' onto the stack"""
        self.list.append(item)

    def pop(self):
        """Pop the most recently pushed item from the stack"""
        return self.list.pop()

    def isEmpty(self):
        """Returns true if the stack is empty"""
        return len(self.list) == 0

class Queue:
    """A container with a first-in-first-out (FIFO) queuing policy."""
    def __init__(self):
        self.list = []

    def push(self,item):
        """Enqueue the 'item' into the queue"""
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        """Returns true if the queue is empty"""
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

class SearchProblem(abc.ABC):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    @abc.abstractmethod
    def getStartState(self) -> "State":
        """
        Returns the start state for the search problem.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def isGoalState(self, state: "State") -> bool:
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def getSuccessors(self, state: "State") -> List[Tuple["State", str, int]]:
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def getCostOfActions(self, actions) -> int:
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        raise NotImplementedError


ACTION_LIST = ["UP", "DOWN", "LEFT", "RIGHT"]

class State:

    def __init__(self, coordinates, visitedResidences, listOfActions):
        self.coordinates = coordinates
        self.visitedResidences = visitedResidences
        self.listOfActions = listOfActions

    def getTraversedStates(self):
        return self.traversedStates

    def getVisited(self):
        return self.visitedResidences

    def getVisitedLength(self):
        return len(self.visitedResidences)

    def getListOfActions(self) -> List:
        return self.listOfActions

    def addVisited(self, residence):
        if (residence not in self.visitedResidences):
            self.visitedResidences.add(residence)

    def getCoordinates(self):
        return self.coordinates
    


class GridworldSearchProblem(SearchProblem):
    """
    Fill in these methods to define the grid world search as a search problem.
    Actions are of type `str`. Feel free to use any data type/structure to define your states though.
    In the type hints, we use "State" to denote a data structure that keeps track of the state, and you can use
    any implementation of a "State" you want.
    """
    

    def __init__(self, file):
        
        self.obstacles = set()
        self.residences = set()
        self.startingCoordinates = [0,0]

        f = open(file, 'r')
        lines = f.readlines()

        
        rowandcol = lines[0].split()
        self.rows = int(rowandcol[0])
        self.columns = int(rowandcol[1])

        for lineNumber in range(self.rows):
            thisLineList = lines[lineNumber+1].split()
            for colNumber in range(self.columns):
                if (int(thisLineList[colNumber]) == -1):
                    obstacle = (lineNumber, colNumber)
                    self.obstacles.add(obstacle)
                if (int(thisLineList[colNumber]) == 1):
                    residence = (lineNumber, colNumber)
                    self.residences.add(residence)
        
        lastLine = lines[self.rows+1]
        lastLineList = lastLine.split()

        self.startingCoordinates[0] = int(lastLineList[0])
        self.startingCoordinates[1] = int(lastLineList[1])

        self.numberOfResidences = len(self.residences)



    def getStartState(self) -> "State":
        coordinates = (self.startingCoordinates[0], self.startingCoordinates[1])
        initset = set()
        if coordinates in self.residences:
            initset.add(coordinates)
        startState = State(coordinates, initset, [])
        return startState

   

    def isGoalState(self, state: "State") -> bool:
        fie = state.getVisitedLength()
        foo = self.numberOfResidences
        if state.getVisitedLength() == self.numberOfResidences:
            return True
        else: 
            return False

    def getSuccessors(self, state: "State") -> List[Tuple["State", str, int]]:
        subsequentStates = []
        x = state.getCoordinates()[0]
        y = state.getCoordinates()[1]

        # checking for whether up is a valid state 
        canGoUp = False
        if (x != 0): 
            if (x-1, y) not in self.obstacles: 
                canGoUp = True

        # generating the state when goes up         
        if (canGoUp):
            actions = state.getListOfActions().copy()
            actions.append("UP")

            upState = State((x-1, y), state.getVisited().copy(), actions)
            if ((x-1,y) in self.residences):
                upState.addVisited((x-1,y))
            up = (upState, "UP", 1)
            
            subsequentStates.append(up)

        # checking for whether right is a valid state 
        canGoRight = False
        if (y != self.columns-1): 
            if (x, y+1) not in self.obstacles: 
                canGoRight = True

        # generating the state when goes right         
        if (canGoRight):

            actions = state.getListOfActions().copy()
            actions.append("RIGHT")

            rightState = State((x, y+1), state.getVisited().copy(), actions)
            if ((x,y+1) in self.residences):
                rightState.addVisited((x,y+1))
            right = (rightState, "RIGHT", 1)
            
            subsequentStates.append(right)


        # checking for whether up is a valid state 
        canGoDown = False
        rowssss = self.rows-1
        if (x != rowssss): 
            if (x+1, y) not in self.obstacles: 
                canGoDown = True

        # generating the state when goes up         
        if (canGoDown):

            actions = state.getListOfActions().copy()
            actions.append("DOWN")

            downState = State((x+1, y), state.getVisited().copy(), actions)
            if ((x+1,y) in self.residences):
                downState.addVisited((x+1,y))
            down = (downState, "DOWN", 1)
            
            subsequentStates.append(down)

        # checking for whether left is a valid state 
        canGoLeft = False
        if (y != 0): 
            if (x, y-1) not in self.obstacles: 
                canGoLeft = True

        # generating the state when goes left         
        if (canGoLeft):

            actions = state.getListOfActions().copy()
            actions.append("LEFT")

            leftState = State((x, y-1), state.getVisited().copy(), actions)
            if ((x, y-1) in self.residences):
                leftState.addVisited((x, y-1))
            left = (leftState, "LEFT", 1)
            
            subsequentStates.append(left)


        return subsequentStates


    def getCostOfActions(self, actions: List[str]) -> int:
        return len(actions)


def depthFirstSearch(problem: SearchProblem) -> List[str]:
    startState = problem.getStartState()

    q = Stack()

    visited = set()

    q.push(startState)

    while (not q.isEmpty()):
        offq = q.pop()

        coordinates = offq.getCoordinates()
        frozen = frozenset(offq.getVisited())

        if ((coordinates, frozen) in visited):
            continue

        visited.add((coordinates, frozen))

        if problem.isGoalState(offq):
            return offq.getListOfActions()

        successors = problem.getSuccessors(offq)
        for child in successors: 
            q.push(child[0])

    return []


def breadthFirstSearch(problem: SearchProblem) -> List[str]:
    startState = problem.getStartState()

    q = Queue()

    visited = set()

    q.push(startState)

    while (not q.isEmpty()):
        offq = q.pop()

        coordinates = offq.getCoordinates()
        frozen = frozenset(offq.getVisited())

        if ((coordinates, frozen) in visited):
            continue

        visited.add((coordinates, frozen))

        if problem.isGoalState(offq):
            return offq.getListOfActions()

        successors = problem.getSuccessors(offq)
        for child in successors: 
            q.push(child[0])

    return []


def nullHeuristic(state: "State", problem: Optional[GridworldSearchProblem] = None) -> int:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def simpleHeuristic(state: "State", problem: Optional[GridworldSearchProblem] = None) -> int:
    return problem.numberOfResidences - state.getVisitedLength()


def customHeuristic(state: "State", problem: Optional[GridworldSearchProblem] = None) -> int:
    x = state.getCoordinates()[0]
    y = state.getCoordinates()[1]

    visited = state.getVisited()
    
    distances = set()
    for residence in problem.residences:
        if (residence in visited):
            continue
        manhattandistance = abs(x-residence[0]) + abs(y-residence[1])
        distances.add(manhattandistance)
    
    if (len(distances)==0):
        return 0
    else:
        return min(distances)


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[str]:
    startState = problem.getStartState()

    q = PriorityQueue()

    visited = set()

    q.push(startState, heuristic)

    while (not q.isEmpty()):
        offq = q.pop()

        coordinates = offq.getCoordinates()
        frozen = frozenset(offq.getVisited())

        if ((coordinates, frozen) in visited):
            continue

        visited.add((coordinates, frozen))

        if problem.isGoalState(offq):
            return offq.getListOfActions()

        successors = problem.getSuccessors(offq)
        for child in successors: 
            astarcost = len(child[0].getListOfActions()) + heuristic(child[0], problem)
            q.push(child[0], astarcost)

    return []



if __name__ == "__main__":
    ### Sample Test Cases ###
    # Run the following statements below to test the running of your program
    gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case1.txt") # Test Case 1
    print(depthFirstSearch(gridworld_search_problem))
    print(breadthFirstSearch(gridworld_search_problem))
    print(aStarSearch(gridworld_search_problem))
    
    gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case2.txt") # Test Case 2
    print(depthFirstSearch(gridworld_search_problem))
    print(breadthFirstSearch(gridworld_search_problem))
    print(aStarSearch(gridworld_search_problem))
    
    gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case3.txt") # Test Case 3
    print(depthFirstSearch(gridworld_search_problem))
    print(breadthFirstSearch(gridworld_search_problem))
    print(aStarSearch(gridworld_search_problem))
