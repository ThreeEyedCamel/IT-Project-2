import tkinter as tk
from tkinter import *
import re
import os
from PIL import Image, ImageTk


class MazeEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maze Editor")
        self.grid_width = 40
        self.grid_height = 30
        self.cell_size = 20
        self.canvas_width = (self.grid_width + 2) * self.cell_size
        self.canvas_height = (self.grid_height + 2) * self.cell_size
        self.animation_delay = 500
        # Initialise matrix
        self.maze_matrix = None
        self.create_matrix(self.grid_width, self.grid_height)
        # Initialise canvas
        self.background_image = Image.open(r"icons/background.png").resize(
            (self.canvas_width, self.canvas_height))  # Resize to canvas size
        self.background_image = ImageTk.PhotoImage(self.background_image)
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.initialise_canvas()

        self.old_x = None
        self.old_y = None

        # Start and finish coordinates
        self.start_coords = (-1, -1)
        self.finish_coords = (-1, -1)

        # Images
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
        self.button_draw = tk.Button(self.button_frame, image=self.draw_icon, command=self.draw_mode)
        self.button_draw.grid(row=0, column=0, padx=5, pady=5)
        self.button_label_draw = tk.Label(self.button_frame, text="Draw Obstacle")
        self.button_label_draw.grid(row=1, column=0)

        self.button_place_start = tk.Button(self.button_frame, image=self.start_icon, command=self.place_start_mode)
        self.button_place_start.grid(row=0, column=1, padx=5, pady=5)
        self.button_label_start = tk.Label(self.button_frame, text="Place Start")
        self.button_label_start.grid(row=1, column=1)

        self.button_place_finish = tk.Button(self.button_frame, image=self.finish_icon, command=self.place_finish_mode)
        self.button_place_finish.grid(row=0, column=2, padx=5, pady=5)
        self.button_label_finish = tk.Label(self.button_frame, text="Place Finish")
        self.button_label_finish.grid(row=1, column=2)

        self.button_erase = tk.Button(self.button_frame, image=self.eraser_icon, command=self.erase_mode)
        self.button_erase.grid(row=0, column=3, padx=5, pady=5)
        self.button_label_erase = tk.Label(self.button_frame, text="Erase")
        self.button_label_erase.grid(row=1, column=3)

        self.button_export = tk.Button(self.button_frame, image=self.export_icon, command=self.export_maze)
        self.button_export.grid(row=0, column=5, padx=5, pady=5)
        self.button_label_export = tk.Label(self.button_frame, text="Export Maze")
        self.button_label_export.grid(row=1, column=5)

        self.button_clear = tk.Button(self.button_frame, image=self.clear_icon, command=self.clear_maze)
        self.button_clear.grid(row=0, column=4, padx=5, pady=5)
        self.button_label_clear = tk.Label(self.button_frame, text="Clear Maze")
        self.button_label_clear.grid(row=1, column=4)

        self.button_import = tk.Button(self.button_frame, image=self.import_icon, command=self.import_maze)
        self.button_import.grid(row=0, column=6, padx=5, pady=5)
        self.button_label_import = tk.Label(self.button_frame, text="Import Maze")
        self.button_label_import.grid(row=1, column=6)

        self.button_test_animation = tk.Button(self.button_frame, text="Test Animation", command=self.animate_path_test)
        self.button_test_animation.grid(row=0, column=8, padx=5, pady=5)

        # Drop-down menu
        file_menu_options = os.listdir(os.getcwd() + "/savedCourses")
        self.variable = StringVar()
        self.variable.set(file_menu_options[0])
        file_menu_drop = OptionMenu(self.button_frame, self.variable, *file_menu_options)
        file_menu_drop.grid(row=0, column=7, padx=5, pady=5)

        self.algorithm_parameters = [self.grid_width, self.grid_height, self.maze_matrix,
                                     self.start_coords, self.finish_coords]

    def create_matrix(self, matrix_width, matrix_height):
        print("create matrix")
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
        print("initialise canvas")
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
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
                    self.start_coords = (x, y)
                    print(f"start coord: {x},{y}")
                if self.maze_matrix[y][x] == 3:
                    self.canvas.create_rectangle(square_dims, fill="red")
                    self.finish_coords = (x, y)
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
        """
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

    def disable_buttons(self):
        print("disable buttons")
        self.button_draw.config(state=tk.DISABLED)
        self.button_erase.config(state=tk.DISABLED)
        self.button_place_finish.config(state=DISABLED)
        self.button_place_start.config(state=DISABLED)
        self.button_clear.config(state=DISABLED)
        self.button_import.config(state=DISABLED)
        self.button_export.config(state=DISABLED)
        self.button_test_animation.config(state=DISABLED)

    def enable_buttons(self):
        print("enable buttons")
        self.button_draw.config(state=tk.NORMAL)
        self.button_erase.config(state=tk.NORMAL)
        self.button_place_finish.config(state=NORMAL)
        self.button_place_start.config(state=NORMAL)
        self.button_clear.config(state=NORMAL)
        self.button_import.config(state=NORMAL)
        self.button_export.config(state=NORMAL)
        self.button_test_animation.config(state=NORMAL)

    def draw(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.grid_width + 2 and 0 <= y < self.grid_height + 2:
            # Reset start/finish coords
            if self.maze_matrix[y][x] == 2:
                self.start_coords = (-1, -1)
            if self.maze_matrix[y][x] == 3:
                self.finish_coords = (-1, -1)
            self.maze_matrix[y][x] = 1
            self.canvas.create_rectangle(
                x * self.cell_size,
                y * self.cell_size,
                (x + 1) * self.cell_size,
                (y + 1) * self.cell_size,
                fill="black",
                tags= (f"cell_{x}_{y}", 'maze')
            )

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
            self.canvas.delete(f"cell_{x}_{y}")


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
                    fill="green",
                    tags=(f"cell_{x}_{y}",'maze')
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
                    fill="red",
                    tags=(f"cell_{x}_{y}",'maze')
                )
                print(self.finish_coords)

    def export_maze(self):
        with open("savedCourses/maze.txt", "w") as maze_file:
            for row in self.maze_matrix:
                maze_file.write(str(row) + "\n")
                print(row)

    def clear_maze(self):
        print("cleared")
        self.create_matrix(self.grid_width, self.grid_height)
        self.canvas.delete("maze")
        self.initialise_canvas()
        self.start_coords = (-1, -1)
        self.finish_coords = (-1, -1)

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

    def update_path(self, coordinates):
        print(f"Update cell ({coordinates})")
        self.canvas.create_rectangle(coordinates[0] * self.cell_size,
                                     coordinates[1] * self.cell_size,
                                     (coordinates[0] + 1) * self.cell_size,
                                     (coordinates[1] + 1) * self.cell_size,
                                     fill="grey", outline="grey",
                                     tags=(f"cell_{coordinates[0]}_{coordinates[1]}", 'maze')
                                     )

    def update_searched(self, coordinates):
        print(f"Searched cell ({coordinates})")
        self.canvas.create_rectangle(coordinates[0] * self.cell_size,
                                     coordinates[1] * self.cell_size,
                                     (coordinates[0] + 1) * self.cell_size,
                                     (coordinates[1] + 1) * self.cell_size,
                                     fill="cyan", outline="cyan",
                                     tags=(f"cell_{coordinates[0]}_{coordinates[1]}", 'maze')
                                     )

    def animate_moves(self, moveset, viewset, index=0):
        """
        Animates the 'path' of the agent in grey.

        :param moveset: List of two-integer lists representing coordinates visited by agent
        :type moveset: list[tuple[int]]
        :param viewset: For every move: list of two-integer lists representing coordinates viewed by agent
        :type viewset: list[list[tuple[int]]]
        :param index: Counter
        :type index: int
        :return: None
        """
        print(f"animate move {moveset[index]}, index={index}")
        if index < len(moveset):
            self.update_path(moveset[index])
            self.after(self.animation_delay, self.animate_views, viewset, index)
        # Cheeky way to make sure the next move waits
        self.after(self.animation_delay * (1 + len(viewset[index])), self.animate_moves, moveset, viewset, index + 1)

    def animate_views(self, viewset, index, subindex=0):
        """
        Animates the 'searched' areas of the agent in grey.

        :param viewset: For every move: list of two-integer lists representing coordinates viewed by agent
        :type viewset: list[list[tuple[int]]]
        :param index: References the move that applies to the corresponding viewset
        :type index: int
        :param subindex: References coordinate pairs within viewset
        :type subindex: int
        :return: None
        """
        print(f"animate view {viewset[index][subindex]}, index={index}, subindex={subindex}")
        if subindex < len(viewset[index]):
            self.update_searched(viewset[index][subindex])
        self.after(self.animation_delay, self.animate_views, viewset, index, subindex + 1)

    def animate_path_test(self):
        """
        Test function containing sample move/viewset

        """
        self.disable_buttons()
        moveset = [(2, 2), (2, 3), (2, 4), (2, 5)]
        viewset = [
            [(3, 2), (2, 3)],
            [(1, 3), (2, 4)],
            [(3, 4), (2, 5)],
            [(1, 5), (2, 6)]
        ]
        self.animate_moves(moveset, viewset)
        viewset_length = 0
        for i in range(len(viewset)):
            for _ in viewset[i]:
                viewset_length += 1

        self.after(self.animation_delay * (1 + len(moveset) + viewset_length), self.enable_buttons)


if __name__ == "__main__":
    app = MazeEditor()
    app.mainloop()
