import numpy as np
import random
import matplotlib.animation as animation
import matplotlib.pyplot as plt

# Parametros iniciais
grid_size = 100
nutrient_diffusion = 0.05
threshold = 0.5
new_cell_cost = 0.4
old_cell_cost = 0.2

# Inicialização dos grids
grid = np.zeros((grid_size, grid_size))
grid[50, 50] = 1  # Inicia com uma bactéria no centro
nutrients = np.ones((grid_size, grid_size)) * 5

# Difução de nutrientes
def diffuse_nutrients(nutrients):
    new_nutrients = nutrients.copy()
    for x in range(grid_size):
        for y in range(grid_size):
            neighbors = [
                (x-1, y), (x+1, y), (x, y-1), (x, y+1), 
                (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
            total_nutrient = sum(nutrients[i, j] for i, j in neighbors if 0 <= i < grid_size and 0 <= j < grid_size)
            new_nutrients[x, y] = (1 - nutrient_diffusion) * nutrients[x, y] + nutrient_diffusion * total_nutrient / 8
    return new_nutrients

# calcular crowding k(t)
def calculate_crowding(grid, x, y):
    neighbors = [
        (x-1, y), (x+1, y), (x, y-1), (x, y+1),   
        (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)  ]
    k = sum(1 for i, j in neighbors if 0 <= i < grid_size and 0 <= j < grid_size and grid[i, j] == 1)
    return 1 / (1 + k)  # Inverso da quantidade de vizinhos 

def update(grid,nutrients,threshold):
    new_grid = grid.copy()
    new_nutrients = diffuse_nutrients(nutrients)
    
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            k_t = calculate_crowding(grid, i, j)
            if grid[i, j] == 1:  # Célula ocupada
                # Probabilidade de divisão
                if random.random() < 0.2:
                    if k_t * nutrients[i, j] > threshold:
                        # Escolhe um vizinho aleatório
                        neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
                        valid_neighbors = [(x, y) for x, y in neighbors if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]]
                        if valid_neighbors:
                            new_i, new_j = random.choice(valid_neighbors)
                            new_grid[new_i, new_j] = 1 # Nova célula nasce
                            new_nutrients[i, j] -= new_cell_cost # custo de uma celula criada
                new_nutrients[i, j] -= old_cell_cost
                
            # Probabilidade de morte (ainda sem regra)
            if random.random() < 0.05:
                new_grid[i, j] = 0

    # atualiza os nutrientes
    nutrients = np.maximum(new_nutrients, 0)  
    return new_grid




# Configuração da visualização
fig, ax = plt.subplots()
im = ax.imshow(grid, cmap='Greys', vmin=0, vmax=1)

# Função para atualizar o plot a cada frame da animação
def animate(i):
    global grid
    grid = update(grid, nutrients, threshold)
    im.set_data(grid)
    return im,

# Criando animação
ani = animation.FuncAnimation(fig, animate, frames=50, interval=50)
plt.show()