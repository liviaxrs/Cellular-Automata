import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize the grid
def initialize_grid(size, random=True):
    if random:
        return np.random.choice([0, 1], size*size, p=[0.8, 0.2]).reshape(size, size)
    else:
        grid = np.zeros((size, size), dtype=int)
        # Glider example
        grid[1, 2] = grid[2, 3] = grid[3, 1] = grid[3, 2] = grid[3, 3] = 1
        return grid

# Update the grid
def update(frame_num, img, grid):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            # Count live neighbors
            total = int((grid[i, (j-1)%grid.shape[1]] + grid[i, (j+1)%grid.shape[1]] +
                         grid[(i-1)%grid.shape[0], j] + grid[(i+1)%grid.shape[0], j] +
                         grid[(i-1)%grid.shape[0], (j-1)%grid.shape[1]] + grid[(i-1)%grid.shape[0], (j+1)%grid.shape[1]] +
                         grid[(i+1)%grid.shape[0], (j-1)%grid.shape[1]] + grid[(i+1)%grid.shape[0], (j+1)%grid.shape[1]]))
            
            # Apply Conway's rules
            if grid[i, j] == 1:  # Live cell
                if total < 2 or total > 3:
                    new_grid[i, j] = 0
            elif total == 3:  # Dead cell with exactly 3 neighbors
                new_grid[i, j] = 1

    # Update grid and plot
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img

# Main function
def main():
    size = 50  # Grid size
    grid = initialize_grid(size)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, cmap="binary", interpolation="nearest")
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid), frames=100, interval=100, save_count=50)
    plt.show()

# Run the simulation
main()