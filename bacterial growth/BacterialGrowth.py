import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation

# Parametros
GRID_SIZE = 100               
TIME_STEPS = 30              
NUTRIENT_DIFFUSION = 0.05     # Nutrient diffusion rate (delta)
THRESHOLD = 0.2               # Growth threshold (theta)
NEW_CELL_COST = 0.4           # Nutrient cost for new cell (a1)
OLD_CELL_COST = 0.2           # Nutrient cost for existing cell (a2)
GROWTH_PROBABILITY = 0.2      # Probability of growth at empty sites
M = 1                         # Cell growth occurs every m time steps


grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)  
nutrients = np.random.random((GRID_SIZE, GRID_SIZE))  # Numero aleatorio de nutrientes


# calcular crowding k(t)
def calculate_crowding(grid, x, y):
    neighbors = [
        (x-1, y), (x+1, y), (x, y-1), (x, y+1),   
        (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)  ]
    k = sum(1 for i, j in neighbors if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE and grid[i, j] == 1)
    return 1 / (1 + k)  # Inverso da quantidade de vizinhos 

# Difução de nutrientes
def diffuse_nutrients(nutrients):
    new_nutrients = nutrients.copy()
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            neighbors = [
                (x-1, y), (x+1, y), (x, y-1), (x, y+1), 
                (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
            total_nutrient = sum(nutrients[i, j] for i, j in neighbors if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE)
            new_nutrients[x, y] = (1 - NUTRIENT_DIFFUSION) * nutrients[x, y] + NUTRIENT_DIFFUSION * total_nutrient / 8

    return new_nutrients

# Simulação 
for t in range(TIME_STEPS):
    new_nutrients = diffuse_nutrients(nutrients)
 
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            k_t = calculate_crowding(grid, x, y)
            if grid[x, y] == 0:  # celula vazia
                if random.random() < GROWTH_PROBABILITY and t % M == 0:  
                    if k_t * nutrients[x, y] > THRESHOLD:
                        grid[x, y] = 1  # nova celula nasce
                        new_nutrients[x, y] -= NEW_CELL_COST # custo de uma celula criada
            elif grid[x, y] == 1:  # celula ocupada
                new_nutrients[x, y] -= OLD_CELL_COST  # custo de uma celula já existente

    # atualiza os nutrientes
    nutrients = np.maximum(new_nutrients, 0)  

    # Visualization at each time step
    plt.clf()
    plt.imshow(grid, cmap='Greens', interpolation='none')
    plt.title(f"Bacterial Growth Simulation - Step {t+1}")
    plt.pause(0.5)
    
plt.show()

