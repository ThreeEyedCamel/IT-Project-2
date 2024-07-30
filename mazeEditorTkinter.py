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
        self.canvas.bind("<B1-Motion>", self.draw)
        self.old_x = None
        self.old_y = None
        self.button_export = tk.Button(self, text="Export Maze", command=self.export_maze)
        self.button_clear = tk.Button(self, text="Clear Maze", command=self.clear_maze)
        self.button_export.pack()
        self.button_clear.pack()

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

    def export_maze(self):
        for row in self.maze_matrix:
            print(row)

    def clear_maze(self):
        print("cleared")
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.bind()
        for row in self.maze_matrix:
            for i in row:
                print(i)
            print(row)


if __name__ == "__main__":
    app = MazeEditor()
    app.mainloop()
