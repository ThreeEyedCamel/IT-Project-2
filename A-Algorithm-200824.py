# A* Algorithm
# Date created: 18th August
# Date updated last: 20th August
# Modification date: 18th August Teresa, 20th August Teresa, 20th August Nicky
# Author/s: Teresa Chhabra and Nicky Gerrard
# Notes: Currently working on integrating all functions seamlessly
# Imports
from math import sqrt
import heapq


class Cell():
    def __init__(self):
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
        global GRID_ROWS, GRID_COLUMNS
        GRID_ROWS, GRID_COLUMNS = rows, columns

    # Check if the cell is within the grid - returns boolean
    def valid(row, column):
        # return {(column > 0) and (column < GRID_COLUMNS) and (row > 0) and (row < GRID_ROWS)} #teresa commented this
        return 0 <= row < GRID_ROWS and 0 <= column < GRID_COLUMNS

    # Checks if the destination can be accessed - returns boolean
    def unblocked(grid, row, column):
        return grid[row][column] == 0

    # Checks if we have reached the destination
    def destination_reached(row, column, destination):
        # return destination[0] == row and destination[1] == column #teresa commented this
        return (row, column) == destination

    # Euclidean
    """TODO test"""

    def h_value(row, column, destination):
        dest_x = destination[0]
        dest_y = destination[1]
        # First need to find values of DX and DY
        # DX is how far away on the X axis the destination is from the current position
        DX = dest_x - column
        # DY is how far away on the Y axis the destination is from the current position
        DY = dest_y - row
        # H value using euclidean distanceD
        H_value = sqrt(DX ** 2 + DY ** 2)
        return H_value

    """REMOVE AFTER TESTING IS COMPLETE"""
    # print("current location: 1, 1 Destination: 50, 73") #teresa commented this
    # h_value(1, 1, [50, 73]) #teresa commented this

    """
    Traces the path from end destination to the start location using parent cells 
    Goes through 'cell details' and appends each visited space to the path 
    Formats the path
    Effectively, we have already found the shortest path and are now returning it
    Returns a list of tuples 
    NOTE: Cell details should loop through each cell in the grid and call the Cell function for each one
    """

    def trace_path(destination, cell_details):
        row = destination[0]
        column = destination[1]
        path = []
        while not (cell_details[row][column].p_row == row and cell_details[row][column].p_column == column):
            # Add this one to the path
            path.append((cell_details[row][column].p_row, cell_details[row][column].p_column))
            # Re-assigning
            temp_row = cell_details[row][column].p_row
            row = temp_row
            temp_column = cell_details[row][column].p_column
            column = temp_column
            # print("check trace: the current cell is at row", row, "and column", column) # testing to see if code is going through trace_path #can confirm it is running 20th August
        # Reversing path as we went from destination to source
        path.reverse()
        # Adding the destination in the path
        path.append((destination[0], destination[1]))
        return path
        """REMOVE WHEN TESTING IS COMPLETE"""
        # Printing out the path for testing
        # for i in path:
        # print(i, "->", end="")  # teresa: called trace_path in a_star # when i uncomment this area: it gives me a weird output
        # return path

        # Implementation fo A* Algorithm!! Checks given source and dest are valid and not blocked.
        # inspired by gyg in some places

    def a_star(grid, source, destination, is_valid=None):
        # Checking that the given source and destination locations are valid, that the source and destination are not blocked
        if not A_star_functions.valid(source[0], source[1]) or not A_star_functions.valid(destination[0],
                                                                                          destination[1]):
            print("This is an invalid source or destination.")
            return []
        if not A_star_functions.unblocked(grid, source[0], source[1]) or not A_star_functions.unblocked(grid,
                                                                                                        destination[
                                                                                                            0],
                                                                                                        destination[
                                                                                                            1]):
            print("The source or destination is currently blocked.")
            return []
        # Check we are not already at the destination
        if A_star_functions.destination_reached(source[0], source[1], destination):
            print("You are already at the destination!")
            return [source]
        # Initialise the list to store the visited cells and the details (x and y values) of each cell
        closed_list = [[False for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]
        cell_details = [[Cell() for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]
        # Initialise the start cell details and the list that will contain cells to be visited
        i, j = source
        cell_details[i][j].s_cost = 0.0
        cell_details[i][j].h_cost = A_star_functions.h_value(i, j, destination)
        cell_details[i][j].t_cost = cell_details[i][j].s_cost + cell_details[i][j].h_cost
        cell_details[i][j].p_row = i
        cell_details[i][j].p_column = j

        open_list = [(0.0, i, j)]
        heapq.heapify(open_list)
        found_dest = False  # Initialise the Boolean flag that says if the destination has been reached
        # Loop over the algorithm:
        while open_list:
            _, i, j = heapq.heappop(
                open_list)  # Pop the cell with the smallest f-value (we want this one) from the to be visited list
            closed_list[i][j] = True  # This small f-value cell is placed into the visited list
            # Look at what the next available cell is in all directions (current cell's x and y values with the directions added to it)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # 8 degrees of freedom being implemented but not properly called?? teresa
            for direction in directions:
                next_i, next_j = i + direction[0], j + direction[1]
                # Check the next cell is valid, not blocked, not the destination (If it is, you're done give a success message)
                if A_star_functions.valid(next_i, next_j):
                    if A_star_functions.destination_reached(next_i, next_j, destination):
                        cell_details[next_i][next_j].p_row = i
                        cell_details[next_i][next_j].p_column = j
                        found_dest = True
                        print(
                            "checking if a_star_functions.dest_reached is running")  # testing to see if its being called - can confirm its running
                        return A_star_functions.trace_path(destination, cell_details)  # Calling trace_path function
                    elif not closed_list[next_i][next_j] and A_star_functions.unblocked(grid, next_i, next_j):
                        # Calculate which of the next available cells has the lowest f value
                        g_new = cell_details[i][j].s_cost + 1.0
                        h_new = A_star_functions.h_value(next_i, next_j, destination)
                        f_new = g_new + h_new
                        # If this new cell has the lowest value - add it to the list we want it
                        if cell_details[next_i][next_j].t_cost == float('inf') or cell_details[next_i][
                            next_j].t_cost > f_new:
                            heapq.heappush(open_list, (f_new, next_i, next_j))
                            cell_details[next_i][next_j].t_cost = f_new
                            cell_details[next_i][next_j].s_cost = g_new
                            cell_details[next_i][next_j].h_cost = h_new
                            cell_details[next_i][next_j].p_row = i
                            cell_details[next_i][next_j].p_column = j
            """for direction in range(8):  # 8 degrees of freedom yeehaw
                next_i, next_j = calculate_next_position(i, j, direction)"""
            '''20th august version: trying to fix trace_path and displaying path, logic issues?? testing that by adding degrees of freedom 
            if is_valid(next_i, next_j) and not is_obstacle(next_i, next_j) and not is_visited(next_i, next_j):
                update_cell_details(i, j, next_i, next_j)
            add_to_open_list(next_i, next_j)'''
        # If we cant find the destination - give an unsuccessful message
        if not found_dest:
            print("This program has unfortunately failed to find the destination cell :(")
            return []

    # Implementation of Main Function!!!!!!!!!!!!!!!
    # This defines grid, source and destination all via user input. Runs the algorithm by calling a_star.
    def main():  # ignore the red line lol
        print("Main function has begun")  # testing can be commented
        try:
            # Define the grid - use user input and make sure to update the universal variables grid_rows and grid_columns
            rows = int(input("Enter the number of rows in grid: "))
            columns = int(input("Enter the number of columns in grid: "))
            A_star_functions.grid_size(rows, columns)
            # print("Grid size set to:", rows, "rows and", columns, "columns!")  # testing can be commented

            grid = []
            print("Obstacles = 1 \n"  # Explains to user what obstacles equate to
                  "Empty spaces = 0 \n"  # Explains to user what empty spaces equate to
                  "Enter grid data row by row, with spaces in between.")
            for i in range(rows):
                row_input = input(f"Row {i + 1}: ")
                row = list(map(int, row_input.split()))
                if len(row) != columns:
                    print(
                        "Please note that the number of columns in the row does not match the specified number of columns.")
                grid.append(row)
                # print(f"Grid after adding Row {i + 1}:", grid) # saves so much time to comment this lol

            print("--- \n"
                  "This is the final Grid:", grid, "\n---")

            # Define the source and destination - use user input
            source = tuple(map(int, input("Enter start point (row, column): ").split(',')))
            destination = tuple(map(int, input("Enter end point (row, column): ").split(',')))

            source = (source[0] - 1, source[1] - 1)
            destination = (destination[0] - 1, destination[1] - 1)

            print("---")  # testing purposes - so i can spatially read it
            print(source, "is currently the start point. While", destination, "is the end point.")
            print("---")  # testing purposes - so i can spatially read it

            path = A_star_functions.a_star(grid, source, destination)  # Calling a_star which calls trace_path
            if path:
                print("This is the path using A*: ", path)
            else:
                print("There is unfortunately no path found.")
        except Exception as e:
            print("An error occurred: ", e)


# Run the algorithm by calling a_star
if __name__ == "__main__":
    A_star_functions.main()
