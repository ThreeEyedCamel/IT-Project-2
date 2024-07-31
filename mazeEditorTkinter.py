import tkinter as tk


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
        self.button_draw.pack()

        self.button_place_start = tk.Button(self, text="Place Start", command=self.place_start_mode)
        self.button_place_start.pack()

        self.button_place_finish = tk.Button(self, text="Place Finish", command=self.place_finish_mode)
        self.button_place_finish.pack()

        self.button_export = tk.Button(self, text="Export Maze", command=self.export_maze)
        self.button_export.pack()

        self.button_clear = tk.Button(self, text="Clear Maze", command=self.clear_maze)
        self.button_clear.pack()

    def create_matrix(self, matrix_width, matrix_height):
        print("create matrix")
        self.maze_matrix = [[0 for _ in range(matrix_width)] for _ in range(matrix_height)]
        for line in self.maze_matrix:
            line.insert(0, 1)
            line.append(1)
        self.maze_matrix.append([1 for _ in range(matrix_width + 2)])
        self.maze_matrix.insert(0, [1 for _ in range(matrix_width + 2)])

    def initialise_canvas(self):
        print("initialise matrix")
        for y in range(len(self.maze_matrix)):
            for x in range(len(self.maze_matrix[0])):
                if self.maze_matrix[y][x] == 1:
                    self.canvas.create_rectangle(
                        x * self.cell_size,
                        y * self.cell_size,
                        (x + 1) * self.cell_size,
                        (y + 1) * self.cell_size,
                        fill="black"
                    )

    def draw_mode(self):
        print("draw mode")
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.draw)

    def place_start_mode(self):
        print("place start mode")
        self.canvas.bind("<Button-1>", self.place_start)
        self.canvas.unbind("<B1-Motion>")

    def place_finish_mode(self):
        print("place finish mode")
        self.canvas.bind("<Button-1>", self.place_finish)
        self.canvas.unbind("<B1-Motion>")

    def draw(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
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
            if ((0 <= x < self.grid_width and 0 <= y < self.grid_height)
                    and self.maze_matrix[y][x] == 0):
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
            if ((0 <= x < self.grid_width and 0 <= y < self.grid_height)
                    and self.maze_matrix[y][x] == 0):
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

    def export_maze(self):
        for row in self.maze_matrix:
            print(row)

    def clear_maze(self):
        print("cleared")
        self.create_matrix(self.grid_width, self.grid_height)
        self.canvas.delete("all")
        self.initialise_canvas()
        self.start_coords = [-1, -1]
        self.finish_coords = [-1, -1]


if __name__ == "__main__":
    app = MazeEditor()
    app.mainloop()
