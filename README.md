# Forest Fire Spread Simulator

This project provides a simple 2-D stochastic simulation of forest fire dynamics based on a cellular automaton model.

## Features

* Adjustable grid size and initial tree density
* Probability-based lightning ignition and tree regrowth
* Real-time visualization using Matplotlib animation
* Toroidal (wrap-around) boundary conditions

## Installation

```bash
# Clone the repository or download the source code
cd /path/to/project

# (Optional) create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the simulator with default parameters:

```bash
python forest_fire.py
```

Command-line arguments:

| Argument | Default | Description |
|----------|---------|-------------|
| `--width` | 100 | Grid width |
| `--height` | 100 | Grid height |
| `--tree_density` | 0.6 | Initial proportion of cells containing trees |
| `--p_lightning` | 0.0001 | Probability that a tree ignites spontaneously each step |
| `--p_tree_growth` | 0.01 | Probability that an empty cell regrows a tree each step |
| `--steps` | 200 | Number of animation frames |
| `--interval` | 50 | Delay between frames in milliseconds |

Example with custom parameters:

```bash
python forest_fire.py --width 150 --height 150 \
                      --tree_density 0.55 \
                      --p_lightning 0.0002 \
                      --p_tree_growth 0.02 \
                      --steps 500
```

## Model Description

The simulation uses three discrete cell states:

1. **Empty (white)** – no tree present.
2. **Tree (green)** – a healthy tree.
3. **Burning (red)** – a tree currently on fire.

At every time step, the following rules apply:

1. Burning trees turn into empty cells.
2. A tree catches fire if **any** of its eight neighbours is burning.
3. A tree may also ignite spontaneously with probability `p_lightning` (representing lightning strikes).
4. Empty cells may regrow a tree with probability `p_tree_growth`.

All updates occur simultaneously (synchronous updating). The grid wraps around at the borders (toroidal topology).

## License

MIT License. See `LICENSE` for details.