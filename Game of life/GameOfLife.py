import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import linregress

def initialize_grid(size):
    return np.random.choice([0, 1], size*size, p=[0.8, 0.2]).reshape(size, size)

# dimensão de Kolmogorov 
def kolmogorov_dimension(grid):
    sizes = [2, 4, 8, 16]  # Box sizes
    counts = []

    for size in sizes:
        count = 0
        for i in range(0, grid.shape[0], size):
            for j in range(0, grid.shape[1], size):
                if np.any(grid[i:i+size, j:j+size]):
                    count += 1
        counts.append(count)
    
    
    log_sizes = np.log(1 / np.array(sizes))
    log_counts = np.log(counts)
    slope, _, _, _, _ = linregress(log_sizes, log_counts)
    
    return slope

# Atualizando grid
def update(frame_num, img, grid,ax, dimensions):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            # contando o total de vizinhos
            total = int((grid[i, (j-1)%grid.shape[1]] + grid[i, (j+1)%grid.shape[1]] +
                         grid[(i-1)%grid.shape[0], j] + grid[(i+1)%grid.shape[0], j] +
                         grid[(i-1)%grid.shape[0], (j-1)%grid.shape[1]] + grid[(i-1)%grid.shape[0], (j+1)%grid.shape[1]] +
                         grid[(i+1)%grid.shape[0], (j-1)%grid.shape[1]] + grid[(i+1)%grid.shape[0], (j+1)%grid.shape[1]]))
            
            # Aplicação de regras (Conway's rules)
            if grid[i, j] == 1:  # Celula viva
                if total < 2 or total > 3:
                    new_grid[i, j] = 0
            elif total == 3:  # Celula morta e com exatamente 3 vizinhos
                new_grid[i, j] = 1

    # Calculando a dimensão de kolmogorov e atualizando o grid
    dimension = kolmogorov_dimension(new_grid)
    dimensions.append(dimension)

    img.set_data(new_grid)
    ax.set_title(f"Frame: {frame_num}, Kolmogorov Dimension: {dimension:.2f}")
    grid[:] = new_grid[:]
    return img



# Função principal
def main():
    size = 100  # Tamanho do grid
    grid = initialize_grid(size)
    dimensions = []

    fig, ax = plt.subplots()
    img = ax.imshow(grid, cmap="binary", interpolation="nearest")
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, ax, dimensions), frames=100, interval=100, save_count=50)
    plt.show()

# Run the simulation
main()