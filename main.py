import matplotlib.pyplot as plt
import numpy as np

class MazeSolver:
    def __init__(self):
        # Initialize the maze properties
        self.n = 0  # Size of the maze
        self.maze = [[0 for _ in range(self.n)] for _ in range(self.n)]  # Initialize the maze grid
        self.start_x = self.start_y = -1  # Default starting position (not set)
        self.goal_x = self.goal_y = -1  # Default goal position (not set)
        self.path = []  # List to store the coordinates of the path taken

    def read_maze(self, filename):
        # Read the maze from a specified file
        with open(filename, 'r') as f:
            self.n = int(f.readline().strip())  # Read the size of the maze
            self.maze = []  # Initialize the maze as an empty list
            for i in range(self.n):
                line = f.readline().strip()  # Read each line of the maze
                row = []  # Initialize a new row for the maze
                for j, char in enumerate(line):
                    # Determine the content of each cell based on the character
                    if char == 'S':
                        self.start_x, self.start_y = i, j  # Store start position
                        row.append(0)  # Mark start position as a path
                    elif char == 'G':
                        self.goal_x, self.goal_y = i, j  # Store goal position
                        row.append(0)  # Mark goal position as a path
                    elif char == '#':
                        row.append(1)  # Wall represented by 1
                    else:
                        row.append(0)  # Path represented by 0
                self.maze.append(row)  # Add the constructed row to the maze

    def display_maze(self):
        # Print the maze in the console for debugging or visualization
        for row in self.maze:
            print(' '.join(map(str, row)))  # Join row elements with a space and print

    def solve_maze(self, x, y):
        # Recursive function to solve the maze using backtracking
        if x == self.goal_x and y == self.goal_y:
            self.path.append((x, y))  # Add the goal to the path
            return True  # Goal reached

        # Check if the current position is valid for movement
        if self.is_valid_move(x, y):
            self.maze[x][y] = 2  # Mark the current cell as part of the path
            self.path.append((x, y))  # Add this position to the path

            # Explore in all four directions
            if (self.solve_maze(x + 1, y) or   # Move down
                self.solve_maze(x - 1, y) or   # Move up
                self.solve_maze(x, y + 1) or   # Move right
                self.solve_maze(x, y - 1)):     # Move left
                return True  # If any direction leads to the goal

            # Backtrack if no path is found
            self.maze[x][y] = 0  # Unmark the cell as part of the path
            self.path.pop()  # Remove this position from the path if backtracking

        return False  # Return False if no valid path is found

    def is_valid_move(self, x, y):
        # Check if a move to the cell (x, y) is valid
        return (0 <= x < self.n and
                0 <= y < self.n and
                self.maze[x][y] != 1 and  # Ensure it's not a wall
                self.maze[x][y] != 2)      # Ensure it hasn't been visited

    def visualize(self):
        # Create a visualization of the maze
        figure_scale = 0.75  # Scale factor to adjust the figure size
        plt.figure(figsize=(self.n * figure_scale, self.n * figure_scale), facecolor='white')  # White background for the figure
        maze_array = np.array(self.maze)  # Convert the maze list to a numpy array for easier processing

        # Set the axes background color to white
        plt.gca().set_facecolor('white')

        # Draw the walls of the maze
        for x in range(self.n):
            for y in range(self.n):
                if maze_array[x][y] == 1:  # If it's a wall
                    plt.gca().add_patch(plt.Rectangle((y, x), 1, 1, fill=True, edgecolor='white', facecolor='black', linewidth=1))

        # Draw the path taken in white
        if self.path:
            path_x, path_y = zip(*self.path)  # Unzip path coordinates
            path_x = np.array(path_x)  # Convert to numpy array for element-wise operations
            path_y = np.array(path_y)
            plt.plot(path_y + 0.5, path_x + 0.5, color='black', linewidth=2)  # Draw path as a line
            # Set the path cells to white
            for (x, y) in self.path:
                plt.gca().add_patch(plt.Rectangle((y, x), 1, 1, color='white'))

        # Mark the start and goal positions
        plt.scatter(self.start_y + 0.5, self.start_x + 0.5, marker='o', color='green', s=100, label='Start (S)')
        plt.scatter(self.goal_y + 0.5, self.goal_x + 0.5, marker='x', color='red', s=100, label='Goal (G)')

        # Draw the outline around the maze
        plt.gca().add_patch(plt.Rectangle((0, 0), self.n, self.n, fill=False, edgecolor='black', linewidth=2))

        # Set the aspect of the plot to be equal
        plt.xlim(0, self.n)  # Set x limits
        plt.ylim(self.n, 0)  # Set y limits (invert y-axis to match maze coordinates)

        # Add a legend and title
        plt.legend()
        plt.title('Maze Visualization')
        plt.axis('off')  # Turn off the axis
        plt.show()  # Display the plot

# Example usage
if __name__ == "__main__":
    solver = MazeSolver()  # Create an instance of MazeSolver
    solver.read_maze("maze.txt")  # Read the maze from a file
    solver.display_maze()  # Print the maze in the console

    # Solve the maze starting from the start position
    if solver.solve_maze(solver.start_x, solver.start_y):
        print("Path found!")  # Indicate that a path was found
        solver.visualize()  # Display the maze visualization with start and goal
    else:
        print("No path found.")  # Indicate that no path was found
