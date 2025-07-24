# Parallel Wildfire Simulation Example

This example extends the basic wildfire demo with:

* `weather.h` — structure holding atmospheric data.
* `wildfire_parallel.[hc]` — OpenMP-accelerated, weather-aware wildfire step.
* `test_wildfire.c` — small console program simulating 60 s of wildfire activity.

## Build (GCC / Clang)

Make sure OpenMP is available (add the appropriate flag for your compiler):

```bash
# GCC
gcc -O2 -fopenmp \
    test_wildfire.c wildfire_parallel.c wildfire.c fire_water.c \
    -o test_wildfire
```

Run the simulation:

```bash
./test_wildfire | cat
```

The program prints the count of active fire sources every second while demonstrating growth, suppression, and hose activation.