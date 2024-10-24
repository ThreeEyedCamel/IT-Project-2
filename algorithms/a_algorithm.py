#   A* Algorithm File
#   Last Update: 22nd October 2024, 9:26 PM AEST
#######################################################################################
#   Authors: Teresa Chhabra & Dominique (Nicky) Gerrard
#   Testing & Debugging Conducted by: Teresa Chhabra
#   Additional Bug Fixing & Error Debugging: Dominique (Nicky) Gerrard 
#   Integration with GUI: Hugo Sinden, Teresa Chhabra, Dominique (Nicky) Gerrard
#######################################################################################

# Imports
from math import sqrt
import heapq
import threading
import time
import numpy as np

#Class to define the cell's attributes
class Cell:
    def __init__(self):
        self.p_row = -1  #Parent cell's row index
        self.p_column = -1  #Parent cell's column index
        self.t_cost = float('inf')  #Total cost of the cell (g + h)
        self.s_cost = float('inf')  #Cost from start to this cell
        self.h_cost = 0  #Heuristic cost from this cell to destination

#Grid dimensions variables
GRID_ROWS = 0
GRID_COLUMNS = 0

#Custom set the grid size - call this function after acquiring user input
def grid_size(rows, columns):
    global GRID_ROWS, GRID_COLUMNS
    GRID_ROWS, GRID_COLUMNS = rows, columns

#Check if the cell is within the grid - returns boolean
def valid(row, column):
    return 0 <= row < GRID_ROWS and 0 <= column < GRID_COLUMNS 

#Checks if the destination can be accessed - returns boolean
def unblocked(grid, row, col): 
    return grid[row][col] != 1 


#Checks if we have reached the destination
def dest_reach(row, column, destination):
    return (row, column) == destination

#Heuristic value using the Euclidean algorithm
def h_value(row, column, destination):
    dest_x = destination[0]
    dest_y = destination[1]
    DX = dest_x - column #DX is how far away on the X axis the destination is from the current position
    DY = dest_y - row #DY is how far away on the Y axis the destination is from the current position
    return sqrt(DX ** 2 + DY ** 2)

#Function to trace the path A* took through the maze
def trace_path(end, cell_details):
    path = []
    row, col = end
    while not (cell_details[row][col].p_row == row and cell_details[row][col].p_column == col):
        path.append((col, row)) 
        temp_row = cell_details[row][col].p_row
        temp_col = cell_details[row][col].p_column
        row, col = temp_row, temp_col
    path.append((col, row))  
    return path[::-1]  

#A* Function: This checks given source and dest are valid and not blocked.

def algorithm(grid, start, end):
    explored_points_all = []
    for x, row in enumerate(grid):
        for y, value in enumerate(row):
            if value ==1 and x !=0 and x!=31 and y!=41 and y !=0:
                print (f"location: {x}, {y}")
    print(grid)

    #Defining the start, end and grid
    start = start[::-1]
    print("The start node is:", start)
    end = end[::-1]
    
    grid_size(rows=len(grid), columns=len(grid[1]))  # Set grid size
    print(f"rows: {GRID_ROWS}\ncolumns: {GRID_COLUMNS}")

    # Check that the given source and destination locations are valid, that the source and destination are not blocked
    print(f"Start valid: {valid(start[0], start[1])}\nEnd valid: {valid(end[0], end[1])}")
    if not valid(start[0], start[1]) or not valid(end[0], end[1]):
        raise Exception(f"Invalid source or destination\n Source: {start}\n Destination: {end}")

    # Check we are not already at the destination
    if dest_reach(start[0], start[1], end):
        print("You are already at the destination!")
        return [start]
    
    closed_list = [[False for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]
    cell_details = [[Cell() for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)] 
    print(f"grid columns{GRID_COLUMNS}, grid rows{GRID_ROWS}")

    #Initialise the start cell details and the list that will contain cells to be visited
    i, j = start
    print(f"FIRST i{i}, j{j}")
    cell_details[i][j].p_row = i
    cell_details[i][j].p_column = j
    cell_details[i][j].s_cost = 0.0
    cell_details[i][j].h_cost = h_value(i, j, end)
    cell_details[i][j].t_cost = cell_details[i][j].s_cost + cell_details[i][j].h_cost
    

    open_list = [(0.0, i, j)]
    
    heapq.heapify(open_list)
    found_dest = False  #Initialise the Boolean flag that says if the destination has been reached

    #Loop over the algorithm:
    while open_list:
        _, i, j = heapq.heappop(open_list)  #Pop the cell with the smallest f-value (we want this one) from the to be visited list
        closed_list[i][j] = True  #This small f-value cell is placed into the visited list
        #Look at what the next available cell is in all directions (current cell's x and y values with the directions added to it)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in directions:
            next_i, next_j = i + direction[0], j + direction[1]
            # Check the next cell is valid, not blocked, not the destination (If it is, you're done give a success message)
            if valid(next_i, next_j) == True and unblocked(grid, next_i, next_j) == True: 
                if dest_reach(next_i, next_j, end):
                    print(f"Destination reached: ({next_i},{next_j})")  # Debug
                    print(f"LAST i: {i}, j: {j}")
                    cell_details[next_i][next_j].p_row = i
                    cell_details[next_i][next_j].p_column = j
                    found_dest = True
                    print(trace_path(end, cell_details))
                    
                    return trace_path(end, cell_details), explored_points_all  # Calling trace_path function
                elif not closed_list[next_i][next_j] and unblocked(grid, next_i, next_j):
                    #Calculate which of the next available cells has the lowest f value
                    g_new = cell_details[i][j].s_cost + (1.0 if direction[0] == 0 or direction[1] == 0 else sqrt(2))
                    h_new = h_value(next_i, next_j, end)
                    f_new = g_new + h_new
                    #If this new cell has the lowest value - add it to the list
                    if cell_details[next_i][next_j].t_cost == float('inf') or cell_details[next_i][
                        next_j].t_cost > f_new:
                        heapq.heappush(open_list, (f_new, next_i, next_j))
                        cell_details[next_i][next_j].t_cost = f_new
                        cell_details[next_i][next_j].s_cost = g_new
                        cell_details[next_i][next_j].h_cost = h_new
                        cell_details[next_i][next_j].p_row = i
                        cell_details[next_i][next_j].p_column = j
    #If we cant find the destination - send an unsuccessful message
    if not found_dest:
        print("This program has unfortunately failed to find the destination cell :(")
        return None, explored_points_all

#In order to run this algorithm, pass a_star the grid, source and destination