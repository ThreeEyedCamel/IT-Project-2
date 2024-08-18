from math import sqrt
import heapq

class Cell:
    def __init__(self):
        self.p_column = 0  # Parent cell's column index
        self.t_cost = float('inf')  # Total cost of the cell (g + h)
        self.s_cost = float('inf')  # Cost from start to this cell
        self.h_cost = 0  # Heuristic cost from this cell to destination

GRID_ROWS = 0
GRID_COLUMNS = 0

class A_star_functions:

    @staticmethod
    def grid_size(rows, columns):
        global GRID_ROWS, GRID_COLUMNS
        GRID_ROWS, GRID_COLUMNS = rows, columns
        print(f"Grid size set to: {GRID_ROWS} rows and {GRID_COLUMNS} columns!")

    @staticmethod
    def valid(row, column):
        return 0 <= row < GRID_ROWS and 0 <= column < GRID_COLUMNS

    @staticmethod
    def unblocked(grid, row, column):
        return grid[row][column] == 0

    @staticmethod
    def destination_reached(row, column, destination):
        return (row, column) == destination

    @staticmethod
    def h_value(row, column, destination):
        dest_x, dest_y = destination
        DX = dest_x - column
        DY = dest_y - row
        return sqrt(DX ** 2 + DY ** 2)

    @staticmethod
    def trace_path(destination, cell_details):
        row, column = destination
        path = []
        while (cell_details[row][column].p_row, cell_details[row][column].p_column) != (row, column):
            path.append((cell_details[row][column].p_row, cell_details[row][column].p_column))
            row, column = cell_details[row][column].p_row, cell_details[row][column].p_column
        path.reverse()
        path.append(destination)
        return path

    @staticmethod
    def a_star(grid, source, destination):
        if not A_star_functions.valid(source[0], source[1]) or not A_star_functions.valid(destination[0], destination[1]):
            print("Invalid source or destination.")
            return []
        if not A_star_functions.unblocked(grid, source[0], source[1]) or not A_star_functions.unblocked(grid, destination[0], destination[1]):
            print("Source or destination is blocked.")
            return []
        if A_star_functions.destination_reached(source[0], source[1], destination):
            print("Already at the destination!")
            return [source]

        closed_list = [[False for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]
        cell_details = [[Cell() for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]

        i, j = source
        cell_details[i][j].s_cost = 0.0
        cell_details[i][j].h_cost = A_star_functions.h_value(i, j, destination)
        cell_details[i][j].t_cost = cell_details[i][j].s_cost + cell_details[i][j].h_cost
        cell_details[i][j].p_row = i
        cell_details[i][j].p_column = j

        open_list = [(0.0, i, j)]
        heapq.heapify(open_list)
        found_dest = False

        while open_list:
            _, i, j = heapq.heappop(open_list)
            closed_list[i][j] = True

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for direction in directions:
                next_i, next_j = i + direction[0], j + direction[1]
                if A_star_functions.valid(next_i, next_j):
                    if A_star_functions.destination_reached(next_i, next_j, destination):
                        cell_details[next_i][next_j].p_row = i
                        cell_details[next_i][next_j].p_column = j
                        found_dest = True
                        return A_star_functions.trace_path(destination, cell_details)
                    elif not closed_list[next_i][next_j] and A_star_functions.unblocked(grid, next_i, next_j):
                        g_new = cell_details[i][j].s_cost + 1.0
                        h_new = A_star_functions.h_value(next_i, next_j, destination)
                        f_new = g_new + h_new

                        if cell_details[next_i][next_j].t_cost == float('inf') or cell_details[next_i][next_j].t_cost > f_new:
                            heapq.heappush(open_list, (f_new, next_i, next_j))
                            cell_details[next_i][next_j].t_cost = f_new
                            cell_details[next_i][next_j].s_cost = g_new
                            cell_details[next_i][next_j].h_cost = h_new
                            cell_details[next_i][next_j].p_row = i
                            cell_details[next_i][next_j].p_column = j
        if not found_dest:
            print("Failed to find the destination cell.")
            return []

    @staticmethod
    def main():
        print("Main function has begun")  # testing can be commented
        try:
            # Define the grid - use user input and make sure to update the universal variables grid_rows and grid_columns
            rows = int(input("Enter the number of rows in grid: "))
            columns = int(input("Enter the number of columns in grid: "))
            A_star_functions.grid_size(rows, columns)

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
                print(f"This is how your grid looks after adding Row {i + 1}:", grid)

            # Define the sources and destinations
            num_paths = int(input("Enter the number of paths to find: "))
            sources = []
            destinations = []
            for i in range(num_paths):
                source = tuple(map(int, input(f"Enter source {i + 1} (row, column): ").split(',')))
                print("This worked")
                destination = tuple(map(int, input(f"Enter destination {i + 1} (row, column): ").split(',')))
                sources.append((source[0] - 1, source[1] - 1))
                destinations.append((destination[0] - 1, destination[1] - 1))

            print("This is the current Grid: ", grid)

            for index, (source, destination) in enumerate(zip(sources, destinations), start=1):
                print(f"Finding path from source {index} {source} to destination {index} {destination}")
                path = A_star_functions.a_star(grid, source, destination)
                if path:
                    print(f"Path {index} using A*: ", path)
                else:
                    print(f"There is unfortunately no path found for path {index}.")
        except Exception as e:
            print("An error occurred: ", e)


if __name__ == "__main__":
    A_star_functions.main()
