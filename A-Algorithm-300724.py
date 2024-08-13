# A* Algorithm
# Date created: 30th July
# Modification date:3rd August Nicky, 4th August Teresa, 6th August Nicky 
# Author/s: Teresa Chhabra and Nicky Gerrard
# SLAYYYYyyyYYYYyyyy

# Imports

from math import sqrt


class Cell():
    def _init_(self):
        # NOTE:THIS IS DIRECTLY FROM G4G AS I DONT KNOW HOW TO REWRITE IT
        # this seems to be the universal way to declare so maybe we can change the names really - renamed
        self.p_row = 0  # Parent cell's row index
        self.p_column = 0  # Parent cell's column index
        self.t_cost = float('inf')  # Total cost of the cell (g + h)
        self.s_cost = float('inf')  # Cost from start to this cell
        self.h_cost = 0  # Heuristic cost from this cell to destination


GRID_ROWS = 0
GRID_COLUMNS = 0

class A_star_functions():
    
    # Custom set the grid size - call this function after acquiring user input
    def grid_size(rows, columns):
        # global GRID_ROWS, GRID_COLUMNS = rows, columns # do not necessarily need to have global, but allows us to change the value later
        GRID_ROWS, GRID_COLUMNS = rows, columns


    # Check if the cell is within the grid - returns boolean
    def valid(row, column):
        return {(column > 0) and (column < GRID_COLUMNS) and (row > 0) and (row < GRID_ROWS)}


    # Checks if the destination can be accessed - returns boolean
    def unblocked(grid, row, column):
        return grid[row][column] == 0


    # Checks if we have reached the destination
    def destination_reached(row, column, destination):
        return destination[0] == row and destination[1] == column


    """###################⬇️ TO DO ⬇️#####################"""

    ##NICKY TO DO
    # Euclidean 
    """TODO test"""
    def h_value(row, column, destination):
        dest_x = destination[0]
        dest_y = destination[1]
        # First need to find values of DX and DY
        #DX is how far away on the X axis the destination is from the current position
        DX = dest_x - column 
        #DY is how far away on the Y axis the destination is from the current position
        DY = dest_y - row
        #H value using euclidean distanceD
        H_value = sqrt(DX**2+DY**2)
        print("H value: ", H_value)
        return H_value

    print("current location: 1, 1 Destination: 50, 73")
    h_value(1, 1, [50, 73])


    # Not 100% sure how to do this yet
    """
    Traces the path from end destination to the start location using parent cells 
    Goes through 'cell details' and appends each visited space to the path 
    Formats the path

    NOTE: Cell details should loop through each cell in the grid and call the Cell function for each one
    """

    ## NICKY TO DO
    def trace_path(destination, cell_details):
        print("Trace path function")


    # h_value needs to be called here but for now can comment out
    # Insert the A star function here
    """
    Implements the actual A* algorithm by: 
    Checking that the given source and destination locations are valid, that the source and destination are not blocked 
    Check we are not already at the destination 
    Initialise the list to store the visited cells and the details (x and y values) of each cell 
    Initialise the start cell details and the list that will contain cells to be visited 
    Initialise the Boolean flag that says if the destination has been reached 
    Loop over the algorithm: 
        Pop the cell with the smallest f-value (we want this one) from the to be visited list 
        This small f-value cell is placed into the visited list 
        Look at what the next available cell is in all directions (current cell's x and y values with the directions added to it) 
        Check the next cell is valid, not blocked, not the destination (If it is, you're done give a success message) 
        Calculate which of the next available cells has the lowest f value 
        If this new cell has the lowest value - add it to the list we want it 
    If we cant find the destination - give an unsuccessful message 
    """

    ## TERESA TO DO
    def a_star(grid, source, destination, row, column):
        print("A star function")


    # Main function
    """
        Define the grid - use user input and make sure to update the universal variables grid_rows and grid_columns
        Define the source and destination - use user input
        Run the algorithm by calling a_star
    """

    ##TERESA TO DO
    # trace_path needs to be called here but for now can comment out
    def main(): 
        print("Main function")  # testing purposes
        # defining the grid using user input - text based atm
        rows = int(input("why hello enter rows in grid: "))
        columns = int(input("enter columns in grid: "))
        print(
            "enter grid - 0 for free cell, 1 for obstacle cell, 2 for ..., 3 for ...")  # number allocations for what does what, double check with group charter