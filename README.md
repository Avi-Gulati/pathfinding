# Gnome Garden Robot Pathfinder

## pathfinding
This project is a part of my portfolio for Harvard's CS 182: Artificial Intelligence. It implements various search algorithms to navigate a robot through a garden grid to visit gnome residences. The garden is represented as a 2D grid where each cell can be free, an obstacle (vegetable), or a gnome residence. The objective is for the robot to find an efficient path that visits all gnome residences at least once. The project explores depth-first search (DFS), breadth-first search (BFS), and A* search algorithms, alongside custom heuristic functions for path optimization.

## running the project 

To run the project and solve a garden grid, use the following command:
```  
  python pathfinder.py --input garden_input.txt
```

## functionality
* __DFS and BFS__: These algorithms explore the garden grid to find a path that visits all gnome residences. DFS uses a stack-based approach favoring depth, while BFS uses a queue to explore the nearest unvisited nodes first.
* __A Search*__: Implements A* search algorithm utilizing heuristics to find the most efficient path.
* __Heuristics__: Includes a simple heuristic based on the number of unvisited residences and a custom heuristic that evaluates the minimum Manhattan distance to the nearest unvisited residence to guide the A* search more effectively.
* __Gridworld Problem Definition__: Formalizes the garden navigation as a search problem where states represent the robot's position and visited residences.
