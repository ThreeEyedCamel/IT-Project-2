import numpy as np
import random
import matplotlib.pyplot as plt
def algorithm(grid, start, end):
    # Helper function to check if a point is inside the maze and not an obstacle
    def is_free(x, y):
        return 0 <= x < maze.shape[0] and 0 <= y < maze.shape[1] and maze[x, y] != 1

    # Check for obstacles along the line between two points
    def check_line_collision(p1, p2, step_size=1):
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while (x1, y1) != (x2, y2):
            if not is_free(x1, y1):
                return False
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        return is_free(x2, y2)

    # Distance function
    def distance(p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # RRT algorithm with smaller steps and collision checks along the path
    def rrt(maze, start, goal, max_iterations=10000, step_size=2, goal_bias=0.1):
        tree = {start: None}  # Dictionary to store tree (point: parent)
        points = [start]  # List of points in the tree
        explored_points_all = []  # List to store ALL explored points

        for iteration in range(max_iterations):
            # With some probability, sample the goal to bias the tree towards the goal
            if random.random() < goal_bias:
                random_point = goal
            else:
                # Sample random point
                random_point = (random.randint(0, maze.shape[0] - 1), random.randint(0, maze.shape[1] - 1))

            # Find the nearest point in the tree to the random point
            nearest_point = min(points, key=lambda p: distance(p, random_point))

            # Move from nearest point towards random point
            direction = np.array(random_point) - np.array(nearest_point)
            norm = np.linalg.norm(direction)
            if norm == 0:
                continue
            direction = (direction / norm * step_size).astype(int)  # Normalize and convert to int for movement in grid

            new_point = tuple(np.array(nearest_point) + direction)

            # Add the point to the list of explored points (no reset here)
            explored_points_all.append(new_point)

            # Check if the path between the nearest point and the new point is obstacle-free
            if check_line_collision(nearest_point, new_point, step_size=1) and new_point not in tree:
                tree[new_point] = nearest_point
                points.append(new_point)

                # Print progress every 100 iterations
                if iteration % 100 == 0:
                    print(f"Iteration {iteration}: Point added {new_point}")

                # If new point is near the goal, terminate
                if distance(new_point, goal) < step_size:
                    tree[goal] = new_point
                    return tree, explored_points_all

        return None, explored_points_all  # If no path is found

    # Visualise the maze, the explored points, and the final path
    def plot_maze(maze, path, explored_points_all):
        # Find the start and destination points
        start = tuple(map(int, np.argwhere(maze == 2)[0]))  # Start point (2)
        goal = tuple(map(int, np.argwhere(maze == 3)[0]))  # Goal point (3)

        plt.imshow(maze, cmap='gray_r')

        # Plot all explored points (entire list)
        if explored_points_all:
            explored_x, explored_y = zip(*explored_points_all)
            plt.scatter(explored_y, explored_x, color='yellow', label='Explored Points', s=10)

        # Plot final path
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, color='blue', linewidth=2, label='Final Path')

        # Mark start and goal
        plt.scatter(start[1], start[0], color='green', label='Start')
        plt.scatter(goal[1], goal[0], color='red', label='Goal')

        plt.legend()
        plt.show()

    def convert_maze(maze):
        return np.asarray(maze)

    def run_rrt(maze):
        # Find the start and destination points
        start = tuple(map(int, np.argwhere(maze == 2)[0]))  # Start point (2)
        goal = tuple(map(int, np.argwhere(maze == 3)[0]))  # Goal point (3)

        # Run RRT algorithm
        tree, explored_points_all = rrt(maze, start, goal)

        # Check if a path was found and extract it
        if tree is not None:
            path = extract_path(tree, start, goal)
            print("Path found:", path)
            plot_maze(maze, path, explored_points_all)  # Visualize maze and exploration
            return path, explored_points_all
        else:
            raise Exception("No path found.")

    def extract_path(tree, start, goal):
        path = [goal]
        current = goal
        while current != start:
            current = tree[current]
            path.append(current)
        return path[::-1]  # Reverse the path to go from start to goal

    maze = convert_maze(grid)
    path, explored_points_all = run_rrt(maze)

    for i in range(len(explored_points_all)):
        explored_points_all[i] = explored_points_all[i][::-1]

    for i in range(len(path)):
        path[i] = path[i][::-1]  # Reverse x and y for final path

    return path, explored_points_all