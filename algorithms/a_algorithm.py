# last updated 30th sep teresa
# nicky updated 2nd oct
# teresa updating 3rd oct 

from math import sqrt
import heapq
import threading
import time
import numpy as np

class Cell:
    def __init__(self):
        #NICKY BELOW
        """self.p_row = 0  # Parent cell's row index
        self.p_column = 0  # Parent cell's column index"""
        self.p_row = -1  # Parent cell's row index
        self.p_column = -1  # Parent cell's column index
        self.t_cost = float('inf')  # Total cost of the cell (g + h)
        self.s_cost = float('inf')  # Cost from start to this cell
        self.h_cost = 0  # Heuristic cost from this cell to destination

GRID_ROWS = 0
GRID_COLUMNS = 0

# Custom set the grid size - call this function after acquiring user input
def grid_size(rows, columns):
    global GRID_ROWS, GRID_COLUMNS
    GRID_ROWS, GRID_COLUMNS = rows, columns

# Check if the cell is within the grid - returns boolean
def valid(row, column):
    # print(f"row: {row}, GRID_ROWS: {GRID_ROWS}\ncolumn: {column}, GRID_COLUMNS: {GRID_COLUMNS}")
    #return 0 <= row < GRID_ROWS and 0 <= column < GRID_COLUMNS #TERESA
    ## TERESA BELOW TESTING ##
    within_bounds = (0 <= row < GRID_ROWS) and (0 <= column < GRID_COLUMNS)
    print(f"Checking valid: ({row}, {column}) within bounds: {within_bounds}")
    return within_bounds


# Checks if the destination can be accessed - returns boolean
#NICKY
"""def unblocked(grid, row, column):
    return grid[row][column] == 0"""
def unblocked(grid, column, row):
    #print(f"CURRENT ROW COL{row},{column},{grid[row][column]}")
    #return grid[row][column] == 0 #TERESA 
    ## TERESA BELOW TESTING ##
    is_unblocked = grid[row][column] == 0  # assuming 0 is a free cell
    print(f"Checking unblocked: ({row}, {column}) is {'free' if is_unblocked else 'an obstacle'}")
    return is_unblocked


# Checks if we have reached the destination
def dest_reach(row, column, destination):
    # return destination[0] == row and destination[1] == column #teresa commented this
    return (row, column) == destination

# Heuristic value using the Euclidean algorithm
def h_value(row, column, destination):
    dest_x = destination[0]
    dest_y = destination[1]
    DX = dest_x - column # DX is how far away on the X axis the destination is from the current position
    DY = dest_y - row # DY is how far away on the Y axis the destination is from the current position
    return sqrt(DX ** 2 + DY ** 2)
#NICKY
def trace_path(end, cell_details):
    path = []
    row, col = end
    while not (cell_details[row][col].p_row == row and cell_details[row][col].p_column == col):
        path.append((col, row))
        temp_row = cell_details[row][col].p_row
        temp_col = cell_details[row][col].p_column
        row, col = temp_row, temp_col
    path.append((col, row))  # Add the start node to the path
    return path[::-1]  # Reverse the path to get it from start to end

"""def trace_path(destination, cell_details):
    
    print("Cell details", type(cell_details)) #NICKY
    print("destination", destination) #NICKY
    row = destination[0]
    column = destination[1]
    path = []
    while not (cell_details[row][column].p_row == row and cell_details[row][column].p_column == column):
        cell = (cell_details[row][column].p_row, cell_details[row][column].p_column)  #Start edit cells
        print("path", path)#NICKY
        print(f"Cell length: {len(cell)}")#Nicky
        path.append(cell[::-1])  # Add this one to the path
        temp_row = cell_details[row][column].p_row # Re-assigning
        row = temp_row
        temp_column = cell_details[row][column].p_column
        column = temp_column

    print("WHAT",path) #NICKY
    path.reverse()  # Reversing path as we went from destination to source
    #path.append(start)
    path.append((destination[0], destination[1])) # Adding the destination in the path # just changed
    # print(f"reconstructed path: {path}") # testing
    print(path)
    print(f"path length: {len(path)}")
    return path"""

"""def a_star(grid, start, end):
    print("Starting A* algorithm...")
    start = start[::-1]
    end = end[::-1]

    grid_size(rows=len(grid), columns=len(grid[1]))  # Set grid size
    print(f"Grid size: {GRID_ROWS} x {GRID_COLUMNS}")

    if not valid(start[0], start[1]) or not valid(end[0], end[1]):
        raise Exception(f"Invalid source or destination\n Source: {start}\n Destination: {end}")

    if dest_reach(start[0], start[1], end):
        print("You are already at the destination!")
        return [start]

    closed_list = [[False for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]
    cell_details = [[Cell() for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]

    i, j = start
    cell_details[i][j].s_cost = 0.0
    cell_details[i][j].h_cost = h_value(i, j, end)
    cell_details[i][j].t_cost = cell_details[i][j].s_cost + cell_details[i][j].h_cost
    cell_details[i][j].p_row = i
    cell_details[i][j].p_column = j

    open_list = [(0.0, i, j)]
    heapq.heapify(open_list)

    while open_list:
        _, i, j = heapq.heappop(open_list)
        closed_list[i][j] = True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in directions:
            next_i, next_j = i + direction[0], j + direction[1]
            if valid(next_i, next_j):
                if dest_reach(next_i, next_j, end):
                    print(f"Destination reached at ({next_i}, {next_j})")
                    cell_details[next_i][next_j].p_row = i
                    cell_details[next_i][next_j].p_column = j
                    return trace_path(end, cell_details)
                elif not closed_list[next_i][next_j] and unblocked(grid, next_i, next_j):
                    g_new = cell_details[i][j].s_cost + (1.0 if direction[0] == 0 or direction[1] == 0 else sqrt(2))
                    h_new = h_value(next_i, next_j, end)
                    f_new = g_new + h_new

                    if cell_details[next_i][next_j].t_cost == float('inf') or cell_details[next_i][next_j].t_cost > f_new:
                        heapq.heappush(open_list, (f_new, next_i, next_j))
                        cell_details[next_i][next_j].t_cost = f_new
                        cell_details[next_i][next_j].s_cost = g_new
                        cell_details[next_i][next_j].h_cost = h_new
                        cell_details[next_i][next_j].p_row = i
                        cell_details[next_i][next_j].p_column = j
        #print(f"Open list size: {len(open_list)}")  # Debugging the open list size
    raise Exception("No path found.")
"""

def a_star(grid, start, end):
    print(grid)
    #A* Function: This checks given source and dest are valid and not blocked.

    #NICKY - this is the reason the coords are backwards in ASTAR
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
    
    #i, j = start#NICKY
    # Initialise the list to store the visited cells and the details (x and y values) of each cell
    closed_list = [[False for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]
    cell_details = [[Cell() for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)] 
    #cell_details = [] #NICKY
    print(f"grid columns{GRID_COLUMNS}, grid rows{GRID_ROWS}")#NICKY
    #print(f"Cell details: {cell_details}")#NICKY

    # Initialise the start cell details and the list that will contain cells to be visited
    i, j = start
    print(f"FIRST i{i}, j{j}")#nicky
    cell_details[i][j].p_row = i
    cell_details[i][j].p_column = j
    cell_details[i][j].s_cost = 0.0
    cell_details[i][j].h_cost = h_value(i, j, end)
    cell_details[i][j].t_cost = cell_details[i][j].s_cost + cell_details[i][j].h_cost
    

    open_list = [(0.0, i, j)]
    
    heapq.heapify(open_list)
    found_dest = False  # Initialise the Boolean flag that says if the destination has been reached

    # Loop over the algorithm:
    while open_list:
        _, i, j = heapq.heappop(open_list)  # Pop the cell with the smallest f-value (we want this one) from the to be visited list
        #print(f"Current node: ({i}, {j})") # testing
        closed_list[i][j] = True  # This small f-value cell is placed into the visited list
        # Look at what the next available cell is in all directions (current cell's x and y values with the directions added to it)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in directions:
            next_i, next_j = i + direction[0], j + direction[1]
            # Check the next cell is valid, not blocked, not the destination (If it is, you're done give a success message)
            if valid(next_i, next_j) == True and unblocked(grid, next_i, next_j) == True: #Nicky added == true and unblocked
                # print(f"Neighbour : ({next_i}, {next_j})") # testing
                if dest_reach(next_i, next_j, end):
                    print(f"Destination reached: ({next_i},{next_j})")  # Debug
                    print(f"LAST i: {i}, j: {j}")#nicky
                    cell_details[next_i][next_j].p_row = i
                    cell_details[next_i][next_j].p_column = j
                    found_dest = True
                    #print("checking if a_star_functions.dest_reached is running")  # testing
                    """a = trace_path(end, cell_details)#Nicky
                    print(f"trace path: {a}")#Nicky"""
                    #print(f"open list: {open_list}")#nicky
                    #Nicky below
                    """for i in cell_details:
                        print(f"PRINTING CELL{cell_details[next_i][next_j].p_row}")""" #NICKY
                    print(trace_path(end, cell_details))#Nicky
                    
                    return trace_path(end, cell_details)  # Calling trace_path function
                elif not closed_list[next_i][next_j] and unblocked(grid, next_i, next_j):
                    # Calculate which of the next available cells has the lowest f value
                    g_new = cell_details[i][j].s_cost + (1.0 if direction[0] == 0 or direction[1] == 0 else sqrt(2))
                    h_new = h_value(next_i, next_j, end)
                    f_new = g_new + h_new
                    # If this new cell has the lowest value - add it to the list we want it
                    #print(f"Updating node ({next_i}, {next_j}) with g={g_new}, h={h_new}, f={f_new}") # testing
                    if cell_details[next_i][next_j].t_cost == float('inf') or cell_details[next_i][
                        next_j].t_cost > f_new:
                        heapq.heappush(open_list, (f_new, next_i, next_j))
                        cell_details[next_i][next_j].t_cost = f_new
                        cell_details[next_i][next_j].s_cost = g_new
                        cell_details[next_i][next_j].h_cost = h_new
                        cell_details[next_i][next_j].p_row = i
                        cell_details[next_i][next_j].p_column = j
                        #print(f"Next i: {i}, next j: {j}")#NICKY
    # If we cant find the destination - give an unsuccessful message
    if not found_dest:
        raise Exception("This program has unfortunately failed to find the destination cell :(")


"""THIS FUNCTION IS NOT REQUIRED FOR MAZE INTEGRATION"""
"""Main FUNCTION: This defines grid, source and destination all via user input. Runs the algorithm by calling a_star."""
"""def main():  # ignore the red line lol
    try:
        # Define the grid - use user input and make sure to update the universal variables grid_rows and grid_columns
        rows = int(input("Enter the number of rows in grid: "))
        columns = int(input("Enter the number of columns in grid: "))
        grid_size(rows, columns)
        # print("Grid size set to:", rows, "rows and", columns, "columns!")  # testing

        grid = []
        print("Obstacles = 1 \n"  # Explains to user what obstacles equate to
              "Empty spaces = 0 \n"  # Explains to user what empty spaces equate to
              "Enter grid data row by row, with spaces in between.")
        for i in range(rows):
            row_input = input(f"Row {i + 1}: ")
            row = list(map(int, row_input.split()))
            if len(row) != columns:
                print("Please note that the number of columns in the row does not match the specified number of columns.")
            grid.append(row)
            # print(f"Grid after adding Row {i + 1}:", grid) # testing

        # Define the source and destination - use user input
        source = tuple(map(int, input("Enter start point (row, column): ").split(',')))
        destination = tuple(map(int, input("Enter end point (row, column): ").split(',')))

        source = (source[0] - 1, source[1] - 1)
        destination = (destination[0] - 1, destination[1] - 1)

        # testing:
        # print("---")  # testing purposes - so i can spatially read it
        # print(source, "is currently the start point. While", destination, "is the end point.")
        # print("---")  # testing purposes - so i can spatially read it

        path = a_star(grid, source, destination)  # Calling a_star which calls trace_path
        if path:
            print("This is the path using A*: ", path)
        else:
            print("There is unfortunately no path found.")
    except Exception as e:
        print("An error occurred: ", e)"""


# In order to run this algorithm, pass a_star the grid, source and destination\
