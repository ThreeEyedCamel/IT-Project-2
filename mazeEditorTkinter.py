import tkinter as tk
from tkinter import *
import re
import os


class MazeEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maze Editor")
        self.grid_width = 40
        self.grid_height = 30
        self.cell_size = 20
        self.canvas_width = (self.grid_width + 2) * self.cell_size
        self.canvas_height = (self.grid_height + 2) * self.cell_size
        # Initialise matrix
        self.maze_matrix = None
        self.create_matrix(self.grid_width, self.grid_height)
        # Initialise canvas
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()
        self.initialise_canvas()

        self.old_x = None
        self.old_y = None

        # Start and finish coordinates
        self.start_coords = [-1, -1]
        self.finish_coords = [-1, -1]

        # Buttons
        self.button_draw = tk.Button(self, text="Draw Obstacle", command=self.draw_mode)
        self.button_draw.pack(side="left")

        self.button_place_start = tk.Button(self, text="Place Start", command=self.place_start_mode)
        self.button_place_start.pack(side="left")

        self.button_place_finish = tk.Button(self, text="Place Finish", command=self.place_finish_mode)
        self.button_place_finish.pack(side="left")

        self.button_erase = tk.Button(self, text="Erase", command=self.erase_mode)
        self.button_erase.pack(side="left")

        self.button_export = tk.Button(self, text="Export Maze", command=self.export_maze)
        self.button_export.pack(side="right")

        self.button_clear = tk.Button(self, text="Clear Maze", command=self.clear_maze)
        self.button_clear.pack(side="right")

        self.button_import = tk.Button(self, text="Import Matrix From File", command=self.import_maze)
        self.button_import.pack(side="right")

        # Drop-down menu
        file_menu_options = os.listdir(os.getcwd() + "/savedCourses")

        self.variable = StringVar()
        self.variable.set(file_menu_options[0])
        file_menu_drop = OptionMenu(self, self.variable, *file_menu_options)
        file_menu_drop.pack(side="right")

    def create_matrix(self, matrix_width, matrix_height):
        print("create matrix")
        self.maze_matrix = [[0 for _ in range(matrix_width)] for _ in range(matrix_height)]
        for line in self.maze_matrix:
            line.insert(0, 1)
            line.append(1)
        self.maze_matrix.append([1 for _ in range(matrix_width + 2)])
        self.maze_matrix.insert(0, [1 for _ in range(matrix_width + 2)])

    def initialise_canvas(self):
        print("initialise canvas")
        for y in range(len(self.maze_matrix)):
            for x in range(len(self.maze_matrix[0])):
                square_dims = (x * self.cell_size,
                               y * self.cell_size,
                               (x + 1) * self.cell_size,
                               (y + 1) * self.cell_size)
                if self.maze_matrix[y][x] == 1:
                    self.canvas.create_rectangle(square_dims, fill="black")
                if self.maze_matrix[y][x] == 2:
                    self.canvas.create_rectangle(square_dims, fill="green")
                    self.start_coords = [x, y]
                    print(f"start coord: {x},{y}")
                if self.maze_matrix[y][x] == 3:
                    self.canvas.create_rectangle(square_dims, fill="red")
                    self.finish_coords = [x, y]
                    print(f"finish coord: {x},{y}")

    def draw_mode(self):
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

    def button_modes_template(self, button, function):
        """"
        Honestly this one is kinda useless.
        """
        if button.config('relief')[-1] == 'sunken':
            button.config(relief="raised")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<Button-1>")

        else:
            self.raise_all_buttons()
            button.config(relief="sunken")
            self.canvas.bind("<B1-Motion>", function)
            self.canvas.bind("<Button-1>", function)

    def raise_all_buttons(self):
        self.button_draw.config(relief="raised")
        self.button_place_start.config(relief="raised")
        self.button_place_finish.config(relief="raised")
        self.button_erase.config(relief="raised")

    def draw(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.grid_width + 2 and 0 <= y < self.grid_height + 2:
            self.maze_matrix[y][x] = 1
            self.canvas.create_rectangle(
                x * self.cell_size,
                y * self.cell_size,
                (x + 1) * self.cell_size,
                (y + 1) * self.cell_size,
                fill="black"
            )

    def place_start(self, event):
        if (self.start_coords[0] < 0) and (self.start_coords[1] < 0):
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            if 1 <= x < self.grid_width + 1 and 1 <= y < self.grid_height + 1:
                self.maze_matrix[y][x] = 2
                self.start_coords = [x, y]
                self.canvas.create_rectangle(
                    x * self.cell_size,
                    y * self.cell_size,
                    (x + 1) * self.cell_size,
                    (y + 1) * self.cell_size,
                    fill="green"
                )
                print(self.start_coords)

    def place_finish(self, event):
        if (self.finish_coords[0] < 0) and (self.finish_coords[1] < 0):
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            if 1 <= x < self.grid_width + 1 and 1 <= y < self.grid_height + 1:
                self.finish_coords = [x, y]
                self.maze_matrix[y][x] = 3
                self.canvas.create_rectangle(
                    x * self.cell_size,
                    y * self.cell_size,
                    (x + 1) * self.cell_size,
                    (y + 1) * self.cell_size,
                    fill="red"
                )
                print(self.finish_coords)

    def erase(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 1 <= x < self.grid_width + 1 and 1 <= y < self.grid_height + 1:
            # Reset start/finish coords
            if self.maze_matrix[y][x] == 2:
                self.start_coords = [-1, -1]
            if self.maze_matrix[y][x] == 3:
                self.finish_coords = [-1, -1]
            self.maze_matrix[y][x] = 0
            self.canvas.create_rectangle(
                x * self.cell_size,
                y * self.cell_size,
                (x + 1) * self.cell_size,
                (y + 1) * self.cell_size,
                fill="white", outline="white"
            )

    def export_maze(self):
        with open("savedCourses/maze.txt", "w") as maze_file:
            for row in self.maze_matrix:
                maze_file.write(str(row) + "\n")
                print(row)

    def clear_maze(self):
        print("cleared")
        self.create_matrix(self.grid_width, self.grid_height)
        self.canvas.delete("all")
        self.initialise_canvas()
        self.start_coords = [-1, -1]
        self.finish_coords = [-1, -1]

    def import_maze(self):
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

    def update_path(self, x, y):
        print(f"Update cell ({x},{y})")
        self.canvas.create_rectangle(
            x * self.cell_size,
            y * self.cell_size,
            (x + 1) * self.cell_size,
            (y + 1) * self.cell_size,
            fill="grey", outline="grey"
        )


if __name__ == "__main__":
    app = MazeEditor()
    app.mainloop()
