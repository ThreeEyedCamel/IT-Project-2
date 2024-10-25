import tkinter as tk
import tkinter.messagebox
from tkinter import *
import re
import os
import importlib.util
from PIL import Image, ImageTk


class MazeEditor(tk.Tk):
    """
    Custom tkinter class for an algorithm-testing Graphical User Interface
    """
    def __init__(self):
        super().__init__()
        self.title("Maze Editor")
        # Changeable parameters, measured in cells
        self.grid_width = 40  # Width of grid
        self.grid_height = 30 # Height of grid
        self.cell_size = 20  # Size of cells (smaller = more compressed)
        self.canvas_width = (self.grid_width + 2) * self.cell_size
        self.canvas_height = (self.grid_height + 2) * self.cell_size
        # Animation delays, changes how fast the path/views appear
        self.animation_delay = 100
        self.animation_delay_views = 1
        self.animation_delay_moves = 50
        # Initialise matrix
        self.maze_matrix = None
        self.create_matrix(self.grid_width, self.grid_height)

        # Import background and bush before canvas initialise
        self.background_image = Image.open(r"icons/background.png").resize(
            (self.canvas_width, self.canvas_height))  # Resize to canvas size
        self.background_image = ImageTk.PhotoImage(self.background_image)
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.bush_image = ImageTk.PhotoImage(
            Image.open(r"icons/bush.png", ).resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS))

        # Call canvas initialise
        self.initialise_canvas()

        self.old_x = None
        self.old_y = None

        # Start and finish coordinates
        self.start_coords = (-1, -1)
        self.finish_coords = (-1, -1)

        # Button icon imports
        self.draw_icon = Image.open(r"icons/paintbrush.png").resize((32, 32))
        self.draw_icon = ImageTk.PhotoImage(self.draw_icon)
        self.export_icon = Image.open(r"icons/export.png").resize((32, 32))
        self.export_icon = ImageTk.PhotoImage(self.export_icon)
        self.clear_icon = Image.open(r"icons/trash.png").resize((32, 32))
        self.clear_icon = ImageTk.PhotoImage(self.clear_icon)
        self.eraser_icon = Image.open(r"icons/eraser.png").resize((32, 32))
        self.eraser_icon = ImageTk.PhotoImage(self.eraser_icon)
        self.finish_icon = Image.open(r"icons/finish.png").resize((32, 32))
        self.finish_icon = ImageTk.PhotoImage(self.finish_icon)
        self.start_icon = Image.open(r"icons/start.png").resize((32, 32))
        self.start_icon = ImageTk.PhotoImage(self.start_icon)
        self.import_icon = Image.open(r"icons/import.png").resize((32, 32))
        self.import_icon = ImageTk.PhotoImage(self.import_icon)

        # Create a frame at the bottom of the window for buttons and labels
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="bottom", fill="x")

        # Buttons and labels in a grid layout
        # Draw button
        self.button_draw = tk.Button(self.button_frame, image=self.draw_icon, command=self.draw_mode)
        self.button_draw.grid(row=0, column=0, padx=5, pady=5)
        self.button_label_draw = tk.Label(self.button_frame, text="Draw Obstacle")
        self.button_label_draw.grid(row=1, column=0)

        # Place start button
        self.button_place_start = tk.Button(self.button_frame, image=self.start_icon, command=self.place_start_mode)
        self.button_place_start.grid(row=0, column=1, padx=5, pady=5)
        self.button_label_start = tk.Label(self.button_frame, text="Place Start")
        self.button_label_start.grid(row=1, column=1)

        # Place finish button
        self.button_place_finish = tk.Button(self.button_frame, image=self.finish_icon, command=self.place_finish_mode)
        self.button_place_finish.grid(row=0, column=2, padx=5, pady=5)
        self.button_label_finish = tk.Label(self.button_frame, text="Place Finish")
        self.button_label_finish.grid(row=1, column=2)

        # Eraser mode button
        self.button_erase = tk.Button(self.button_frame, image=self.eraser_icon, command=self.erase_mode)
        self.button_erase.grid(row=0, column=3, padx=5, pady=5)
        self.button_label_erase = tk.Label(self.button_frame, text="Erase")
        self.button_label_erase.grid(row=1, column=3)

        # Export maze to file button
        self.button_export = tk.Button(self.button_frame, image=self.export_icon, command=self.export_maze)
        self.button_export.grid(row=0, column=5, padx=5, pady=5)
        self.button_label_export = tk.Label(self.button_frame, text="Export Maze")
        self.button_label_export.grid(row=1, column=5)

        # Clear maze button
        self.button_clear = tk.Button(self.button_frame, image=self.clear_icon, command=self.clear_maze)
        self.button_clear.grid(row=0, column=4, padx=5, pady=5)
        self.button_label_clear = tk.Label(self.button_frame, text="Clear Maze")
        self.button_label_clear.grid(row=1, column=4)

        # Import maze button
        self.button_import = tk.Button(self.button_frame, image=self.import_icon, command=self.import_maze)
        self.button_import.grid(row=0, column=6, padx=5, pady=5)
        self.button_label_import = tk.Label(self.button_frame, text="Import Maze")
        self.button_label_import.grid(row=1, column=6)

        # Execute algo button
        self.button_execute_algorithm = tk.Button(self.button_frame, text="Run Algorithm",
                                                  command=self.execute_algorithm)
        self.button_execute_algorithm.grid(row=0, column=9, padx=5, pady=5)

        # Drop-down menu - courses
        file_menu_options = os.listdir(os.getcwd() + "/savedCourses")
        self.variable = StringVar()
        self.variable.set(file_menu_options[0])
        file_menu_drop = OptionMenu(self.button_frame, self.variable, *file_menu_options)
        file_menu_drop.grid(row=0, column=7, padx=5, pady=5)

        # Drop-down menu - algorithms
        self.algorithm_menu_options = [x[:-3] for x in os.listdir(os.getcwd() + "/algorithms") if
                                       os.path.splitext(x)[1] == '.py']
        self.algo_variable = StringVar()
        self.algo_variable.set(self.algorithm_menu_options[0])
        self.algorithm_menu_drop = OptionMenu(self.button_frame, self.algo_variable, *self.algorithm_menu_options)
        self.algorithm_menu_drop.grid(row=0, column=8, padx=5, pady=5)

        self.algorithm_parameters = [self.grid_width, self.grid_height, self.maze_matrix,
                                     self.start_coords, self.finish_coords]

        # Import path image
        path_image = Image.open(r"icons/gravel.png", )
        path_image = path_image.resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS)
        path_image = ImageTk.PhotoImage(path_image)
        self.path_image = path_image

        # Import searched tile image
        self.cyan_tile = ImageTk.PhotoImage(
            Image.open(r"icons/cyan.png", ).resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS))

    def create_matrix(self, matrix_width, matrix_height):
        """
        Initialises the maze given width and height dimensions.

        :param int matrix_width:
        :param int matrix_height:
        """
        self.maze_matrix = [[0 for _ in range(matrix_width)] for _ in range(matrix_height)]
        # Add boundary walls around the matrix
        for line in self.maze_matrix:
            line.insert(0, 1)
            line.append(1)
        self.maze_matrix.append([1 for _ in range(matrix_width + 2)])
        self.maze_matrix.insert(0, [1 for _ in range(matrix_width + 2)])

    def initialise_canvas(self):
        """
        All details of canvas initialisation go in this function.
        This includes the background images and textures used. 
        To customise the look of the GUI's background use this function. 

        :return:
        """
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        print(type(self.bush_image))
        for y in range(len(self.maze_matrix)):
            for x in range(len(self.maze_matrix[0])):
                square_dims = (x * self.cell_size,
                               y * self.cell_size,
                               (x + 1) * self.cell_size,
                               (y + 1) * self.cell_size)
                if self.maze_matrix[y][x] == 1:
                    # Bush instead of black squares for obstacle cells
                    self.canvas.create_image(
                        x * self.cell_size + self.cell_size // 2,  # Center the image in the cell
                        y * self.cell_size + self.cell_size // 2,
                        image=self.bush_image,
                        tags=(f"cell_{x}_{y}", 'maze', 'special')
                    )
                # Start point
                if self.maze_matrix[y][x] == 2:
                    # Start point is placed in green
                    self.canvas.create_rectangle(square_dims, fill="green", tags=(f"cell_{x}_{y}", 'maze', 'special'))
                    self.start_coords = (x, y)
                    print(f"start coord: {x},{y}")
                # End point
                if self.maze_matrix[y][x] == 3:
                    # End point is in red 
                    self.canvas.create_rectangle(square_dims, fill="red", tags=(f"cell_{x}_{y}", 'maze', 'special'))
                    self.finish_coords = (x, y)
                    print(f"finish coord: {x},{y}")

    def draw_mode(self):
        """
        Connector between draw button and draw function.
        """
        print("draw mode")
        if self.button_draw.config('relief')[-1] == 'sunken':   # Checks if the draw button is currently active
            self.button_draw.config(relief="raised")            # Deactivate draw mode
            self.canvas.unbind("<B1-Motion>")                   # Unbind drawing with mouse
            self.canvas.unbind("<Button-1>")                    # Unbind drawing on click

        else:                                                   # Drawing active
            self.raise_all_buttons()                            # All buttons should be raised
            self.button_draw.config(relief="sunken")            # Make the draw button active
            self.canvas.bind("<B1-Motion>", self.draw)          # Bind draw to motion
            self.canvas.bind("<Button-1>", self.draw)           # Bind draw to click

    def place_start_mode(self):
        """
        Connector between place start button and place start function.
        """
        print("place start mode")
        if self.button_place_start.config('relief')[-1] == 'sunken':    # Checks if the start placement is active
            self.button_place_start.config(relief="raised")             # Deactivate start placement
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<Button-1>")

        else:
            self.raise_all_buttons()
            self.button_place_start.config(relief="sunken")             # Set start placement as active
            self.canvas.bind("<B1-Motion>", self.place_start)
            self.canvas.bind("<Button-1>", self.place_start)

    def place_finish_mode(self):
        """
        Connector between place finish button and place finish function.
        """
        print("place finish mode")
        if self.button_place_finish.config('relief')[-1] == 'sunken':   # Set finish as active
            self.button_place_finish.config(relief="raised")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<Button-1>")

        else:
            self.raise_all_buttons()
            self.button_place_finish.config(relief="sunken")
            self.canvas.bind("<B1-Motion>", self.place_finish)
            self.canvas.bind("<Button-1>", self.place_finish)

    def erase_mode(self):
        """
        Connector between erase button and erase function.
        """
        print("erase mode")
        if self.button_erase.config('relief')[-1] == 'sunken':     # Checks erase mode is active
            self.button_erase.config(relief="raised")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<Button-1>")

        else:
            self.raise_all_buttons()
            self.button_erase.config(relief="sunken")
            self.canvas.bind("<B1-Motion>", self.erase)
            self.canvas.bind("<Button-1>", self.erase)

    def raise_all_buttons(self):
        """
        Connector between place start button and place start function.
        """
        self.button_draw.config(relief="raised")
        self.button_place_start.config(relief="raised")
        self.button_place_finish.config(relief="raised")
        self.button_erase.config(relief="raised")

    def disable_buttons(self):
        """
        Disables clickable buttons during an operation
        """
        print("disable buttons")
        self.button_draw.config(state=tk.DISABLED)
        self.button_erase.config(state=tk.DISABLED)
        self.button_place_finish.config(state=DISABLED)
        self.button_place_start.config(state=DISABLED)
        self.button_clear.config(state=DISABLED)
        self.button_import.config(state=DISABLED)
        self.button_export.config(state=DISABLED)
        self.button_execute_algorithm.config(state=DISABLED)

    def enable_buttons(self):
        """
        Re-enables clickable buttons.
        """
        print("enable buttons")
        self.button_draw.config(state=tk.NORMAL)
        self.button_erase.config(state=tk.NORMAL)
        self.button_place_finish.config(state=NORMAL)
        self.button_place_start.config(state=NORMAL)
        self.button_clear.config(state=NORMAL)
        self.button_import.config(state=NORMAL)
        self.button_export.config(state=NORMAL)
        self.button_execute_algorithm.config(state=NORMAL)

    def draw(self, event):
        """
        Draws an obstacle at the clicked square.

        :param event: x and y coordinates on click
        """
        x = event.x // self.cell_size   # Determine the cell x coordinate
        y = event.y // self.cell_size   # Determine the cell Y coordinate
        if 0 <= x < self.grid_width + 2 and 0 <= y < self.grid_height + 2:
            # Reset start/finish coords (if for example they are drawn over)
            if self.maze_matrix[y][x] == 2:
                self.start_coords = (-1, -1)
            if self.maze_matrix[y][x] == 3:
                self.finish_coords = (-1, -1)
            self.maze_matrix[y][x] = 1  # Set cell as an obstacle
            self.canvas.create_image(
                x * self.cell_size + self.cell_size // 2,  # Center the image in the cell horisontally and vertically
                y * self.cell_size + self.cell_size // 2,
                image=self.bush_image,
                tags=(f"cell_{x}_{y}", 'maze', 'special')
            )

    def erase(self, event):
        """
        Clears the tile at the clicked square.

        :param event: Mouse event providing x and y coordinates.
        """
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 1 <= x < self.grid_width + 1 and 1 <= y < self.grid_height + 1:
            # Reset start/finish coords (if for example they are drawn over)
            if self.maze_matrix[y][x] == 2:
                self.start_coords = (-1, -1)
            if self.maze_matrix[y][x] == 3:
                self.finish_coords = (-1, -1)
            self.maze_matrix[y][x] = 0
            self.canvas.delete(f"cell_{x}_{y}")

    def place_start(self, event):
        """
        Places a green square at the clicked tile.

        :param event: Mouse event containing x and y coordinates of the click.
        """
        # Check if the start coordinates have not been set
        if (self.start_coords[0] < 0) and (self.start_coords[1] < 0):
            # Convert click position to grid coordinates
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            # Ensure the click is within grid bounds
            if 1 <= x < self.grid_width + 1 and 1 <= y < self.grid_height + 1:
                # Set the start position in the maze matrix
                self.maze_matrix[y][x] = 2
                self.start_coords = (x, y)
                # Draw a green square on the canvas at the start position
                self.canvas.create_rectangle(
                    x * self.cell_size,
                    y * self.cell_size,
                    (x + 1) * self.cell_size,
                    (y + 1) * self.cell_size,
                    fill="green",
                    tags=(f"cell_{x}_{y}", 'maze', 'special')
                )
                print(self.start_coords) # Debug print for start coordinates

    def place_finish(self, event):
        """
        Places a red square at the clicked tile.

        :param event: Mouse event containing x and y coordinates of the click.
        """
        # Check if the finish coordinates have not been set
        if (self.finish_coords[0] < 0) and (self.finish_coords[1] < 0):
            # Convert click position to grid coordinates
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            # Ensure the click is within grid bounds
            if 1 <= x < self.grid_width + 1 and 1 <= y < self.grid_height + 1:
                # Set the finish position in the maze matrix
                self.finish_coords = (x, y)
                self.maze_matrix[y][x] = 3
                # Draw a red square on the canvas at the finish position
                self.canvas.create_rectangle(
                    x * self.cell_size,
                    y * self.cell_size,
                    (x + 1) * self.cell_size,
                    (y + 1) * self.cell_size,
                    fill="red",
                    tags=(f"cell_{x}_{y}", 'maze', 'special')
                )
                print(self.finish_coords) # Debug print for finish coordinates

    def export_maze(self, path="maze.txt"):
        """
        Exports the current obstacle and start/finish to a text file.

        :param String path: Filepath for saved file
        """
        with open("savedCourses/" + path, "w") as maze_file:
            for row in self.maze_matrix:
                maze_file.write(str(row) + "\n")  # Write each row of the maze to the file
                print(row)  # Debug print for each row

    def clear_maze(self):
        """
        Clears the current obstacles

        """
        print("cleared") # Debug message
        self.create_matrix(self.grid_width, self.grid_height)   # Reset maze matrix
        self.canvas.delete("maze")  # Remove all maze elements from the canvas
        self.initialise_canvas()  # Reinitialize the canvas
        self.start_coords = (-1, -1)  # Reset the start coordinates
        self.finish_coords = (-1, -1)  # Reset the finish coordinates

    def import_maze(self):
        """
        Imports the maze selected from the maze drop down into the maze.
        """
        import_file_path = "savedCourses/" + self.variable.get()
        print(f"import from text file: {import_file_path}")
        self.maze_matrix = []
        with open(import_file_path, 'r') as maze_file:
            for line in maze_file:
                # for sub in re.split(",", line[1:-2]):
                #     print(int(sub.strip()))
                integer_list = [int(sub.strip()) for sub in re.split(",", line[1:-2])]
                self.maze_matrix.append(integer_list)
        self.canvas.delete("all")  # Clear the canvas
        self.initialise_canvas()  # Reinitialize canvas with imported maze data

    def update_path(self, coordinates):
        """
        Creates a path tile on the specified coordinate

        :param tuple coordinates: Grid position of the path tile.
        """
        cell_tag = f"cell_{coordinates[0]}_{coordinates[1]}"

        items = self.canvas.find_withtag(cell_tag)
        if items:
            for item in items:
                if 'special' in self.canvas.gettags(item):
                    return  # Skip drawing over this cell if it has the 'special' tag
        # Draw path on the canvas
        self.canvas.create_image(coordinates[0] * self.cell_size + self.cell_size // 2,
                                 coordinates[1] * self.cell_size + self.cell_size // 2,
                                 image=self.path_image,
                                 tags=(f"cell_{coordinates[0]}_{coordinates[1]}", 'maze')
                                 )

    def update_searched(self, coordinates):
        """
        Updates specified tile as translucent light blue.

        :param tuple coordinates: Grid position of the searched tile.
        """
        cell_tag = f"cell_{coordinates[0]}_{coordinates[1]}"

        # Check if the cell has the 'special' tag
        items = self.canvas.find_withtag(cell_tag)
        if items:
            for item in items:
                if 'special' in self.canvas.gettags(item):
                    return  # Skip if cell is marked as special
        # Draw searched/looked at places on the canvas
        self.canvas.create_image(coordinates[0] * self.cell_size + self.cell_size // 2,
                                 coordinates[1] * self.cell_size + self.cell_size // 2,
                                 image=self.cyan_tile,
                                 tags=(f"cell_{coordinates[0]}_{coordinates[1]}", 'maze')
                                 )

    def animate_algorithm(self, explored_points_all, path):
        """
        Animate algorithm.

        :param list(tuple) explored_points_all: All explored points by the algorithm.
        :param list(tuple) path: The final path found by the algorithm.
        """
        self.animate_searched_points(explored_points_all, 0, path)

    def animate_searched_points(self, explored_points, index, path):
        """
        Animate searched points.

        :param list(tuple) explored_points: Points explored by the algorithm.
        :param int index: Current index of explored points to display.
        :param list(tuple) path: The final path found by the algorithm.
        """
        if index < len(explored_points):
            self.update_searched(explored_points[index])  # Show the searched tile
            self.after(self.animation_delay_views,
                       lambda: self.animate_searched_points(explored_points, index + 1, path))
        else:
            # Once all searched points are shown, animate the path
            self.animate_path_algorithm(path)

    def animate_path_algorithm(self, path, index=0):
        """
        Animate algorithm path.

        :param list(int) path: The sequence of grid coordinates forming the path.
        :param int index: Current index in the path to display.
        """
        if index < len(path):
            self.update_path(path[index])   # Show the path
            self.after(self.animation_delay_moves, lambda: self.animate_path_algorithm(path, index + 1))

    def execute_algorithm(self):
        """
        Main function for executing algorithm, connects to buttons
        """
        self.disable_buttons()  # Disable buttons during execution

        # Check if start and finish points are defined
        if self.start_coords == (-1, -1) or self.finish_coords == (-1, -1):
            tkinter.messagebox.showerror("Error", "Start and/or Finish not found")
            print("No start and/or end found, exiting...")
            self.enable_buttons()
            return None

        print(self.algo_variable.get())
        # Load and execute the selected algorithm module
        algorithm_file_path = 'algorithms/' + self.algo_variable.get() + '.py'
        algorithm_module_name = self.algo_variable.get()
        print(algorithm_module_name)
        spec = importlib.util.spec_from_file_location(algorithm_module_name, algorithm_file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, 'algorithm'):
            print("Algorithm found, executing...")
            path, explored_points_all = getattr(module, 'algorithm')(self.maze_matrix,
                                                                     self.start_coords, self.finish_coords)

            if path is None:
                tkinter.messagebox.showerror("Error", "No path found.")
                self.enable_buttons()
                return None
            else:
                self.animate_algorithm(explored_points_all, path)

        else:
            tkinter.messagebox.showerror("Error", "Algorithm function not found, please check your algorithm module.")
            print("No algorithm found, exiting...")

        self.enable_buttons()  # Re-enable buttons


if __name__ == "__main__":
    app = MazeEditor()
    app.mainloop()
