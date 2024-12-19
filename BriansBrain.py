import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize the grid
def initialize_brians_brain(size):
    return np.random.choice([0, 1], size * size, p=[0.9, 0.1]).reshape(size, size)

# Update function for Brian's Brain
def update(grid):
    rows, cols = grid.shape
    new_grid = np.zeros((rows, cols), dtype=int)
    for i in range(rows):
        for j in range(cols):
            # Count alive neighbors
            neighbors = sum([
                grid[(i-1) % rows, (j-1) % cols] == 1, grid[(i-1) % rows, j] == 1, grid[(i-1) % rows, (j+1) % cols] == 1,
                grid[i, (j-1) % cols] == 1, grid[i, (j+1) % cols] == 1,
                grid[(i+1) % rows, (j-1) % cols] == 1, grid[(i+1) % rows, j] == 1, grid[(i+1) % rows, (j+1) % cols] == 1
            ])
            
            # Apply Brian's Brain rules
            if grid[i, j] == 0 and neighbors == 2:
                new_grid[i, j] = 1  # Dead -> Alive
            elif grid[i, j] == 1:
                new_grid[i, j] = 2  # Alive -> Dying
            elif grid[i, j] == 2:
                new_grid[i, j] = 0  # Dying -> Dead
    return new_grid

# Main function to run the animation
def main():
    size = 50  # Grid size
    steps = 200  # Number of steps in the animation
    grid = initialize_brians_brain(size)
    
    fig, ax = plt.subplots()
    img = ax.imshow(grid, cmap="viridis", interpolation="nearest")
    plt.axis("off")
    
    def animate(frame):
        nonlocal grid
        grid = update(grid)
        img.set_data(grid)
        return [img]
    
    ani = animation.FuncAnimation(fig, animate, frames=steps, interval=100, blit=True)
    plt.show()

# Run the simulation
main()
