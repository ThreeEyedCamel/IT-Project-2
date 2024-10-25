import heapq
import numpy as np

"""
Dikstras path planning algorithm 
"""
#Defines the 
class Dijkstra:
    def __init__(self, maze_matrix, start, goal):
        self.maze_matrix = maze_matrix                  #Define the grid that holds the maze
        self.grid_width = len(maze_matrix[0]) - 2       #Define grid width
        self.grid_height = len(maze_matrix) - 2         #Define grid height
        self.start = start                              #Define start point
        self.goal = goal                                #Define end point

    #Check if the coordinate is free or blocked
    def is_free(self, x, y):
        return 0 <= x < self.grid_width + 2 and 0 <= y < self.grid_height + 2 and self.maze_matrix[y][x] != 1


    def check_line_collision(self, p1, p2):
        #Get each points coordinates
        x1, y1 = p1
        x2, y2 = p2

        #Calculate differences in x and y, then set the step direction for each axis
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy #Error value to control line direction 

        #Iterate over each point from point 1 to point 2
        while (x1, y1) != (x2, y2):
            if not self.is_free(x1, y1):
                return False #If an obstacle is found return false
            #Adjust error and move in x or y direction based on Bresenham's line algorithm
            e2 = 2 * err
            if e2 > -dy:
                err -= dy #Update error based on Y movement
                x1 += sx #Move a step in X direction
            if e2 < dx:
                err += dx #Update error based on X movement
                y1 += sy #Move a step in Y direction
        #Check the last step (point 2) is available
        return self.is_free(x2, y2)

    #Calculates Euclidean distance between two points  
    def distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


    def extract_path(self, parent_map, start, goal):
        #Create the path with the goal(end destination) as the first point
        path = [goal]
        current = goal #Set the current point as the goal
        #Continue through the parent map until you reach the start from the goal
        while current != start: 
            current = parent_map[current] #Update the parent of the current point
            path.append(current) #Add the new point to the path
        #Reverse path to make it from the start to the goal
        return path[::-1] 

    def dijkstra(self):
        #Initialise the priority queue
        priority_queue = []
        heapq.heappush(priority_queue, (0, self.start)) #Add the distance and the point
        #Initialise the distance distionary and the parent map(used to backtrack steps)
        distances = {self.start: 0}
        parent_map = {self.start: None}
        explored_points_all = []

        #Loop through all points until all reachable nodes are visited or goal is reached
        while priority_queue:
            #Pop the point with the smallest distance from the queue
            current_distance, current_point = heapq.heappop(priority_queue)
            explored_points_all.append(current_point)#Add current point to explored points
            #Check if the destination has been reached
            if current_point == self.goal:
                #Return the reconstructed path and all explored points
                return self.extract_path(parent_map, self.start, self.goal), explored_points_all

            # Explore neighbors, 8 points of movement
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1,-1), (1,-1), (-1,1), (1,1)]:
                neighbor = (current_point[0] + dx, current_point[1] + dy)
                #Check if neighbor is free (no obstacle) and accessible
                if self.is_free(neighbor[0], neighbor[1]) and self.check_line_collision(current_point, neighbor):
                    #Calculate likely distance to the neighbor
                    new_distance = current_distance + self.distance(current_point, neighbor)
                    #If neighbor is unvisited or a shorter path is found
                    if neighbor not in distances or new_distance < distances[neighbor]:
                        #Update distance and parent map with new optimal path
                        distances[neighbor] = new_distance
                        parent_map[neighbor] = current_point
                        #Push neighbor with updated distance to the priority queue
                        heapq.heappush(priority_queue, (new_distance, neighbor))
        #If goal was not reached, return None and all explored points
        return None, explored_points_all


def algorithm(maze_matrix, start_coords, finish_coords):
    #Instantiate the Dijkstra class with maze matrix, start, and finish coordinates
    dijkstra_instance = Dijkstra(maze_matrix, start_coords, finish_coords)
    #'Run the Dijkstra algorithm and return the resulting path and explored points
    return dijkstra_instance.dijkstra()
