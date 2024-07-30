import tkinter as tk


class MazeEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Maze Editor")
        self.canvas_width = 800
        self.canvas_height = 600
        self.cell_size = 20
        self.grid_width = self.canvas_width // self.cell_size
        self.grid_height = self.canvas_height // self.cell_size
        self.maze_matrix = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()
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

    def draw_mode(self):
        print("draw mode")
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.draw)

    def place_start_mode(self):
        print("place start mode")
        self.canvas.bind("<Button-1>", self.place_start)

    def place_finish_mode(self):
        print("place finish mode")
        self.canvas.bind("<Button-1>", self.place_finish)

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
            if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
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
            if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
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
        self.canvas.delete("all")
        self.maze_matrix = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.start_coords = [-1, -1]
        self.finish_coords = [-1, -1]


if __name__ == "__main__":
    app = MazeEditor()
    app.mainloop()
