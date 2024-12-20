import numpy as np
import matplotlib.pyplot as plt

def initialize_grid(size, initial_live_cells):
    grid = np.zeros((size, size), dtype=int)
    live_cells = np.random.randint(0, size * size, initial_live_cells)
    grid[np.unravel_index(live_cells, (size, size))] = 1
    return grid

def count_neighbors(grid, x, y):
    size = grid.shape[0]
    neighbors = (
        grid[x, (y - 1) % size] +  # Top
        grid[x, (y + 1) % size] +  # Bottom
        grid[(x - 1) % size, y] +  # Left
        grid[(x + 1) % size, y] +  # Right
        grid[(x - 1) % size, (y - 1) % size] +  # Top-left
        grid[(x - 1) % size, (y + 1) % size] +  # Bottom-left
        grid[(x + 1) % size, (y - 1) % size] +  # Top-right
        grid[(x + 1) % size, (y + 1) % size]  # Bottom-right
    )
    return neighbors

def update_grid(grid, nutrient_grid, growth_threshold=2, nutrient_diffusion_rate=0.1):

    new_grid = grid.copy()
    new_nutrient_grid = nutrient_grid.copy()

    # Nutrient diffusion
    for i in range(new_nutrient_grid.shape[0]):
        for j in range(new_nutrient_grid.shape[1]):
            neighbors_nutrients = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    nx = (i + dx) % new_nutrient_grid.shape[0]
                    ny = (j + dy) % new_nutrient_grid.shape[1]
                    neighbors_nutrients += new_nutrient_grid[nx, ny]
            new_nutrient_grid[i, j] = new_nutrient_grid[i, j] + nutrient_diffusion_rate * (neighbors_nutrients - 8 * new_nutrient_grid[i, j])

    # Bacterial growth and nutrient consumption
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            neighbors = count_neighbors(grid, x, y)
            if grid[x, y] == 1:  # Live cell
                if neighbors < 2 or neighbors > 3 or new_nutrient_grid[x, y] < 0.1:  # Dies due to underpopulation, overpopulation, or lack of nutrients
                    new_grid[x, y] = 0
                    new_nutrient_grid[x, y] += 0.1  # Release nutrients upon death
            else:  # Dead cell
                if neighbors >= growth_threshold and new_nutrient_grid[x, y] >= 0.5:  # Grows if enough neighbors and sufficient nutrients
                    new_grid[x, y] = 1
                    new_nutrient_grid[x, y] -= 0.5  # Consume nutrients upon growth

    return new_grid, new_nutrient_grid

def simulate(grid, nutrient_grid, num_generations):
    grids = [grid]
    nutrient_grids = [nutrient_grid]
    for _ in range(num_generations):
        grid, nutrient_grid = update_grid(grid, nutrient_grid)
        grids.append(grid.copy())
        nutrient_grids.append(nutrient_grid.copy())
    return grids, nutrient_grids

def visualize(grids, nutrient_grids):
    plt.figure(figsize=(10, 5))  # Adjust the figure size for side-by-side plots

    for i, (grid, nutrient_grid) in enumerate(zip(grids, nutrient_grids)):
        plt.clf()

        # Subplot 1: Bacterial Growth
        plt.subplot(1, 2, 1)
        plt.imshow(grid, cmap='Greens', interpolation='none')
        plt.title(f"Bacterial Growth - Step {i}")
        plt.axis('off')

        # Subplot 2: Nutrient Distribution
        plt.subplot(1, 2, 2)
        plt.imshow(nutrient_grid, cmap='hot', interpolation='none')
        plt.title(f"Nutrient Levels - Step {i}")
        plt.axis('off')

        plt.pause(0.1)  # Pause to update the visualization

    plt.show()


if __name__ == "__main__":
    grid_size = 100
    initial_live_cells = 50
    num_generations = 50

    initial_grid = initialize_grid(grid_size, initial_live_cells)
    initial_nutrient_grid = np.ones((grid_size, grid_size))  # Initialize with uniform nutrient distribution

    grids, nutrient_grids = simulate(initial_grid, initial_nutrient_grid, num_generations)
    visualize(grids, nutrient_grids)