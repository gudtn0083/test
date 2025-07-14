import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Cell states
EMPTY = 0
TREE = 1
BURNING = 2

STATE_COLORS = {
    EMPTY: (1.0, 1.0, 1.0),   # white
    TREE: (0.0, 0.6, 0.0),     # green
    BURNING: (1.0, 0.0, 0.0)   # red
}

# Added: mapping from cardinal directions to grid vectors (dy, dx)
WIND_DIR_VECTORS = {
    'N': (-1, 0),
    'NE': (-1, 1),
    'E': (0, 1),
    'SE': (1, 1),
    'S': (1, 0),
    'SW': (1, -1),
    'W': (0, -1),
    'NW': (-1, -1)
}


def create_initial_forest(width: int, height: int, tree_density: float) -> np.ndarray:
    """Generate an initial forest grid with given tree density."""
    return (np.random.random((height, width)) < tree_density).astype(np.int8)


class ForestFireSimulator:
    def __init__(self,
                 width: int = 100,
                 height: int = 100,
                 tree_density: float = 0.6,
                 p_lightning: float = 0.0001,
                 p_tree_growth: float = 0.01,
                 p_fire_spread: float = 1.0,
                 wind_direction: str | None = None,
                 wind_strength: float = 0.2):
        self.width = width
        self.height = height
        self.p_lightning = p_lightning
        self.p_tree_growth = p_tree_growth
        self.p_fire_spread = p_fire_spread

        # Wind setup
        if wind_direction is None or wind_direction.upper() == 'NONE':
            self.wind_vector: tuple[int, int] | None = None
        else:
            dir_key = wind_direction.upper()
            if dir_key not in WIND_DIR_VECTORS:
                raise ValueError(f"Invalid wind_direction '{wind_direction}'. Choose from {list(WIND_DIR_VECTORS)} or None.")
            self.wind_vector = WIND_DIR_VECTORS[dir_key]
        self.wind_strength = wind_strength

        # Initialize grid: TREE(1) where there is a tree, else EMPTY(0)
        self.grid = create_initial_forest(width, height, tree_density)

    def _neighbor_burning(self, y: int, x: int) -> bool:
        """Check Moore neighborhood (8-neighbors) for burning cells."""
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                ny, nx = (y + dy) % self.height, (x + dx) % self.width
                if self.grid[ny, nx] == BURNING:
                    return True
        return False

    def step(self):
        """Advance the simulation by one time step."""
        new_grid = self.grid.copy()

        # Vectorized operations: process each state separately for speed
        # 1. Burning trees become empty
        burning_mask = self.grid == BURNING
        new_grid[burning_mask] = EMPTY

        # 2. Trees that have burning neighbor ignite
        tree_mask = self.grid == TREE
        # Iterate over trees and check neighbors (vectorization is tricky)
        # We'll use convolution via scipy? But to avoid dependency, fallback to loops over tree indices.
        # Loops over whole grid may be slower but fine for medium sizes.
        tree_indices = np.argwhere(tree_mask)
        for y, x in tree_indices:
            ignited = False
            # Check all neighbours for burning cells and compute wind-biased spread probability
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = (y + dy) % self.height, (x + dx) % self.width
                    if self.grid[ny, nx] != BURNING:
                        continue

                    # Base spread probability
                    p_spread = self.p_fire_spread

                    # Apply wind bias if configured
                    if self.wind_vector is not None:
                        # Vector from burning neighbour to this tree
                        spread_vec = (-dy, -dx)
                        if spread_vec == self.wind_vector:
                            # Down-wind spread: increase probability
                            p_spread = min(1.0, p_spread + self.wind_strength)
                        elif spread_vec == (-self.wind_vector[0], -self.wind_vector[1]):
                            # Up-wind spread: decrease probability
                            p_spread = max(0.0, p_spread - self.wind_strength)
                    if np.random.random() < p_spread:
                        ignited = True
                        break  # No need to check other neighbours
                if ignited:
                    break
            if ignited or (np.random.random() < self.p_lightning):
                new_grid[y, x] = BURNING

        # 3. Empty cells may regrow trees
        empty_mask = self.grid == EMPTY
        regrow = np.random.random((self.height, self.width)) < self.p_tree_growth
        new_grid[empty_mask & regrow] = TREE

        self.grid = new_grid

    def run(self, steps: int = 200, interval: int = 50):
        """Run the simulation with real-time visualization."""
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title('Forest Fire Simulator')
        img = ax.imshow(self._grid_to_rgb(), interpolation='nearest')
        ax.set_axis_off()

        def update(frame):
            self.step()
            img.set_data(self._grid_to_rgb())
            return (img,)

        anim = animation.FuncAnimation(fig, update, frames=steps, interval=interval, blit=True)
        plt.show()

    def _grid_to_rgb(self):
        """Convert the integer grid into an RGB image array for plotting."""
        rgb = np.zeros((self.height, self.width, 3))
        for state, color in STATE_COLORS.items():
            mask = self.grid == state
            rgb[mask] = color
        return rgb


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Forest Fire Spread Simulator')
    parser.add_argument('--width', type=int, default=100, help='Grid width')
    parser.add_argument('--height', type=int, default=100, help='Grid height')
    parser.add_argument('--tree_density', type=float, default=0.6, help='Initial tree density (0-1)')
    parser.add_argument('--p_lightning', type=float, default=0.0001, help='Probability of lightning strike per tree per step')
    parser.add_argument('--p_tree_growth', type=float, default=0.01, help='Probability of tree regrowth per empty cell per step')
    parser.add_argument('--p_fire_spread', type=float, default=1.0, help='Base probability that a burning neighbour ignites a tree (before wind bias)')
    parser.add_argument('--wind_direction', type=str, default=None, help="Wind direction among N, NE, E, SE, S, SW, W, NW; omit for no wind")
    parser.add_argument('--wind_strength', type=float, default=0.2, help='Wind bias amount added/subtracted to base spread probability (0-1)')
    parser.add_argument('--steps', type=int, default=200, help='Number of simulation steps')
    parser.add_argument('--interval', type=int, default=50, help='Interval between frames in milliseconds')

    args = parser.parse_args()

    sim = ForestFireSimulator(width=args.width,
                              height=args.height,
                              tree_density=args.tree_density,
                              p_lightning=args.p_lightning,
                              p_tree_growth=args.p_tree_growth,
                              p_fire_spread=args.p_fire_spread,
                              wind_direction=args.wind_direction,
                              wind_strength=args.wind_strength)
    sim.run(steps=args.steps, interval=args.interval)