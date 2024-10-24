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
        # Changeable parameters
        self.grid_width = 40  # Measured in cells
        self.grid_height = 30
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
        for line in self.maze_matrix:
            line.insert(0, 1)
            line.append(1)
        self.maze_matrix.append([1 for _ in range(matrix_width + 2)])
        self.maze_matrix.insert(0, [1 for _ in range(matrix_width + 2)])

    def initialise_canvas(self):
        """
        All details of canvas initialisation go in this function

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
                    # Bush instead of black squares
                    self.canvas.create_image(
                        x * self.cell_size + self.cell_size // 2,  # Center the image in the cell
                        y * self.cell_size + self.cell_size // 2,
                        image=self.bush_image,
                        tags=(f"cell_{x}_{y}", 'maze', 'special')
                    )
                if self.maze_matrix[y][x] == 2:
                    self.canvas.create_rectangle(square_dims, fill="green", tags=(f"cell_{x}_{y}", 'maze', 'special'))
                    self.start_coords = (x, y)
                    print(f"start coord: {x},{y}")
                if self.maze_matrix[y][x] == 3:
                    self.canvas.create_rectangle(square_dims, fill="red", tags=(f"cell_{x}_{y}", 'maze', 'special'))
                    self.finish_coords = (x, y)
                    print(f"finish coord: {x},{y}")

    def draw_mode(self):
        """
        Connector between draw button and draw function.
        """
        print("draw mode")
        if self.button_draw.config('relief')[-1] == 'sunken':
            self.button_draw.config(relief="raised")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<Button-1>")

        else:
            self.raise_all_buttons()
            self.button_draw.config(relief="sunken")
            self.canvas.bind("<B1-Motion>", self.draw)
            self.canvas.bind("<Button-1>", self.draw)

    def place_start_mode(self):
        """
        Connector between place start button and place start function.
        """
        print("place start mode")
        if self.button_place_start.config('relief')[-1] == 'sunken':
            self.button_place_start.config(relief="raised")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<Button-1>")

        else:
            self.raise_all_buttons()
            self.button_place_start.config(relief="sunken")
            self.canvas.bind("<B1-Motion>", self.place_start)
            self.canvas.bind("<Button-1>", self.place_start)

    def place_finish_mode(self):
        """
        Connector between place finish button and place finish function.
        """
        print("place finish mode")
        if self.button_place_finish.config('relief')[-1] == 'sunken':
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
        if self.button_erase.config('relief')[-1] == 'sunken':
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
        Disables clickable buttons.
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
        :return:
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

        :param event:
        """
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.grid_width + 2 and 0 <= y < self.grid_height + 2:
            # Reset start/finish coords
            if self.maze_matrix[y][x] == 2:
                self.start_coords = (-1, -1)
            if self.maze_matrix[y][x] == 3:
                self.finish_coords = (-1, -1)
            self.maze_matrix[y][x] = 1
            self.canvas.create_image(
                x * self.cell_size + self.cell_size // 2,  # Center the image in the cell
                y * self.cell_size + self.cell_size // 2,
                image=self.bush_image,
                tags=(f"cell_{x}_{y}", 'maze', 'special')
            )

    def erase(self, event):
        """
        Clears the tile at the clicked square.

        :param event:
        """
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 1 <= x < self.grid_width + 1 and 1 <= y < self.grid_height + 1:
            # Reset start/finish coords
            if self.maze_matrix[y][x] == 2:
                self.start_coords = (-1, -1)
            if self.maze_matrix[y][x] == 3:
                self.finish_coords = (-1, -1)
            self.maze_matrix[y][x] = 0
            self.canvas.delete(f"cell_{x}_{y}")

    def place_start(self, event):
        """
        Places a green square at the clicked tile.

        :param event:
        """
        if (self.start_coords[0] < 0) and (self.start_coords[1] < 0):
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            if 1 <= x < self.grid_width + 1 and 1 <= y < self.grid_height + 1:
                self.maze_matrix[y][x] = 2
                self.start_coords = (x, y)
                self.canvas.create_rectangle(
                    x * self.cell_size,
                    y * self.cell_size,
                    (x + 1) * self.cell_size,
                    (y + 1) * self.cell_size,
                    fill="green",
                    tags=(f"cell_{x}_{y}", 'maze', 'special')
                )
                print(self.start_coords)

    def place_finish(self, event):
        """
        Places a red square at the clicked tile.

        :param event:
        """
        if (self.finish_coords[0] < 0) and (self.finish_coords[1] < 0):
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            if 1 <= x < self.grid_width + 1 and 1 <= y < self.grid_height + 1:
                self.finish_coords = (x, y)
                self.maze_matrix[y][x] = 3
                self.canvas.create_rectangle(
                    x * self.cell_size,
                    y * self.cell_size,
                    (x + 1) * self.cell_size,
                    (y + 1) * self.cell_size,
                    fill="red",
                    tags=(f"cell_{x}_{y}", 'maze', 'special')
                )
                print(self.finish_coords)

    def export_maze(self, path="maze.txt"):
        """
        Exports the current obstacle and start/finish to a text file.

        :param String path: Filepath for saved file
        """
        with open("savedCourses/" + path, "w") as maze_file:
            for row in self.maze_matrix:
                maze_file.write(str(row) + "\n")
                print(row)

    def clear_maze(self):
        """
        Clears the current obstacles

        :return:
        """
        print("cleared")
        self.create_matrix(self.grid_width, self.grid_height)
        self.canvas.delete("maze")
        self.initialise_canvas()
        self.start_coords = (-1, -1)
        self.finish_coords = (-1, -1)

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
        self.canvas.delete("all")
        self.initialise_canvas()

    def update_path(self, coordinates):
        """
        Creates a path tile on the specified coordinate

        :param tuple coordinates:
        """
        cell_tag = f"cell_{coordinates[0]}_{coordinates[1]}"

        items = self.canvas.find_withtag(cell_tag)
        if items:
            for item in items:
                if 'special' in self.canvas.gettags(item):
                    return  # Skip drawing over this cell if it has the 'special' tag

        self.canvas.create_image(coordinates[0] * self.cell_size + self.cell_size // 2,
                                 coordinates[1] * self.cell_size + self.cell_size // 2,
                                 image=self.path_image,
                                 tags=(f"cell_{coordinates[0]}_{coordinates[1]}", 'maze')
                                 )

    def update_searched(self, coordinates):
        """
        Updates specified tile as translucent light blue.

        :param tuple coordinates:
        """
        cell_tag = f"cell_{coordinates[0]}_{coordinates[1]}"

        # Check if the cell has the 'special' tag
        items = self.canvas.find_withtag(cell_tag)
        if items:
            for item in items:
                if 'special' in self.canvas.gettags(item):
                    return

        self.canvas.create_image(coordinates[0] * self.cell_size + self.cell_size // 2,
                                 coordinates[1] * self.cell_size + self.cell_size // 2,
                                 image=self.cyan_tile,
                                 tags=(f"cell_{coordinates[0]}_{coordinates[1]}", 'maze')
                                 )

    def animate_algorithm(self, explored_points_all, path):
        """
        Animate algorithm.

        :param list(tuple) explored_points_all:
        :param list(tuple) path:
        """
        self.animate_searched_points(explored_points_all, 0, path)

    def animate_searched_points(self, explored_points, index, path):
        """
        Animate searched points.

        :param list(tuple) explored_points:
        :param int index:
        :param list(tuple) path:
        """
        if index < len(explored_points):
            self.update_searched(explored_points[index])
            self.after(self.animation_delay_views,
                       lambda: self.animate_searched_points(explored_points, index + 1, path))
        else:
            # Once all searched points are shown, animate the path
            self.animate_path_algorithm(path)

    def animate_path_algorithm(self, path, index=0):
        """
        Animate algorithm path.

        :param list(int) path:
        :param int index:
        """
        if index < len(path):
            self.update_path(path[index])
            self.after(self.animation_delay_moves, lambda: self.animate_path_algorithm(path, index + 1))

    def execute_algorithm(self):
        """
        Main function for executing algorithm, connects to buttons
        """
        self.disable_buttons()

        if self.start_coords == (-1, -1) or self.finish_coords == (-1, -1):
            tkinter.messagebox.showerror("Error", "Start and/or Finish not found")
            print("No start and/or end found, exiting...")
            self.enable_buttons()
            return None

        print(self.algo_variable.get())
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

        self.enable_buttons()


if __name__ == "__main__":
    app = MazeEditor()
    app.mainloop()
