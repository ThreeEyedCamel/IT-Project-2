# A* Algorithm
# Date created: 30th July
# Modification date: 3rd August Nicky, 4th August
# Author/s: Teresa Chhabra and Nicky Gerrard
# SLAYYYYyyyYYYY

# Imports

class Cell():
    def _init_ (self):
        # NOTE:THIS IS DIRECTLY FROM G4G AS I DONT KNOW HOW TO REWRITE IT
        # this seems to be the universal way to declare so maybe we can change the names really - renamed
        self.p_row = 0 # Parent cell's row index
        self.p_column = 0 # Parent cell's column index
        self.t_cost = float('inf') # Total cost of the cell (g + h)
        self.s_cost = float('inf') # Cost from start to this cell
        self.h_cost = 0 # Heuristic cost from this cell to destination
GRID_ROWS = 0
GRID_COLUMNS = 0

# Custom set the grid size - call this function after acquiring user input
def grid_size(rows, columns):
    GRID_ROWS, GRID_COLUMNS = rows, columns

# Check if the cell is within the grid - returns boolean
def valid(row, column):
    return {(column>0) and (column<GRID_COLUMNS)and (row>0)and(row<GRID_ROWS)}

# Checks if the destination can be accessed - returns boolean
def unblocked(grid, row, column):
    return grid[row][column] == 0

# Checks if we have reached the destination
def destination_reached(row, column, destination):
    return destination[0] == row and destination[1]== column

"""###################⬇️ TO DO ⬇️#####################"""
# Yet to decide on our H value calculation method
def h_value(row, column, destination):
    print("H value function")

# Not 100% sure how to do this yet
"""
Traces the path from end destination to the start location using parent cells 
Goes through 'cell details' and appends each visited space to the path 
Formats the path

NOTE: Cell details should loop through each cell in the grid and call the Cell function for each one
"""
def trace_path(destination, cell_details):
    print("Trace path function")

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
def a_star():
    print("A star function")

# Main function
"""
    Define the grid - use user input and make sure to update the universal variables grid_rows and grid_columns
    Define the source and destination - use user input
    Run the algorithm by calling a_star
"""
def main():
    print("Main function")
    