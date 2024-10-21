import heapq
import numpy as np


class Dijkstra:
    def __init__(self, maze_matrix, grid_width, grid_height, start, goal):
        self.maze_matrix = maze_matrix
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.start = start
        self.goal = goal

    def is_free(self, x, y):
        return 0 <= x < self.grid_width + 2 and 0 <= y < self.grid_height + 2 and self.maze_matrix[y][x] != 1

    def check_line_collision(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while (x1, y1) != (x2, y2):
            if not self.is_free(x1, y1):
                return False
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        return self.is_free(x2, y2)

    def distance(self, p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def extract_path(self, parent_map, start, goal):
        path = [goal]
        current = goal
        while current != start:
            current = parent_map[current]
            path.append(current)
        return path[::-1]  # Keep the order (x, y) as is

    def dijkstra(self):
        priority_queue = []
        heapq.heappush(priority_queue, (0, self.start))
        distances = {self.start: 0}
        parent_map = {self.start: None}
        explored_points_all = []

        while priority_queue:
            current_distance, current_point = heapq.heappop(priority_queue)
            explored_points_all.append(current_point)

            if current_point == self.goal:
                return self.extract_path(parent_map, self.start, self.goal), explored_points_all

            # Explore neighbors (4-connected grid)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current_point[0] + dx, current_point[1] + dy)

                if self.is_free(neighbor[0], neighbor[1]) and self.check_line_collision(current_point, neighbor):
                    new_distance = current_distance + self.distance(current_point, neighbor)

                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        parent_map[neighbor] = current_point
                        heapq.heappush(priority_queue, (new_distance, neighbor))

        return None, explored_points_all


def algorithm(maze_matrix, grid_width, grid_height, start_coords, finish_coords):
    dijkstra_instance = Dijkstra(maze_matrix, grid_width, grid_height, start_coords, finish_coords)
    return dijkstra_instance.dijkstra()
