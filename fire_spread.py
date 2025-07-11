#!/usr/bin/env python3
"""fire_spread.py
A simple fire spread simulator for a 2D grid.

Usage::
    python fire_spread.py < input.txt

The input format matches the classic wildfire escape problems:
    R C               # number of rows and columns
    ....F             # grid rows, any of . # F J
    ...#.
    .J#..
    ...F.

Legend::
    .  empty cell (burnable)
    #  wall / obstacle (not burnable, fire stops)
    F  initial fire source (burning at time 0)
    J  starting point of the person (treated as empty for fire)

The script prints a time-map showing when each burnable cell catches fire.
Unreachable cells remain as -1.

If run as main, it also computes the earliest escape time for the person
(`J`) assuming they can move up, down, left, right one cell per minute
and cannot enter a cell on or after it burns. If escaping is impossible,
it prints "IMPOSSIBLE".
"""
from __future__ import annotations

import sys
from collections import deque
from typing import List, Tuple, Optional

Coord = Tuple[int, int]
DIRECTIONS: List[Coord] = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# Mapping from single-letter wind notation to direction vector
WIND_VECTORS: dict[str, Coord] = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
}

def read_grid_from_stdin() -> Tuple[List[List[str]], Coord, Optional[Coord]]:
    """Reads the grid and (optionally) a wind direction.

    Returns ``(grid, start_pos, wind_vec)`` where ``wind_vec`` is a direction
    tuple like ``(dx, dy)`` or ``None`` if no wind information is provided.
    """
    line = sys.stdin.readline()
    if not line:
        raise ValueError("Empty input")
    r, c = map(int, line.split())
    grid: List[List[str]] = []
    start: Coord | None = None
    for i in range(r):
        row = list(sys.stdin.readline().rstrip("\n"))
        if len(row) != c:
            raise ValueError(f"Row {i} length {len(row)} != {c}")
        for j, cell in enumerate(row):
            if cell == 'J':
                start = (i, j)
        grid.append(row)
    if start is None:
        raise ValueError("No starting position 'J' found in grid")

    # Try to read an additional line for wind. Empty/EOF → no wind.
    wind_line = sys.stdin.readline()
    wind_vec: Optional[Coord] = None
    if wind_line:
        w = wind_line.strip().upper()
        if w:
            if w not in WIND_VECTORS:
                raise ValueError(f"Unsupported wind direction '{w}'. Use one of {list(WIND_VECTORS.keys())} or leave blank.")
            wind_vec = WIND_VECTORS[w]

    return grid, start, wind_vec


def compute_fire_time(grid: List[List[str]], wind_vec: Optional[Coord] = None) -> List[List[int]]:
    """Returns the minute each cell catches fire, taking *wind* into account.

    The algorithm assigns an integer cost to each spread step:
        • With wind direction → cost = 1 (fastest)
        • Perpendicular to wind → cost = 2
        • Against the wind → cost = 3

    Without wind information, every step costs 1 (identical to the old logic).
    A Dijkstra-style search computes the earliest arrival time at each cell.
    ``-1`` means the cell never burns.
    """
    import math
    from heapq import heappush, heappop

    r, c = len(grid), len(grid[0])
    INF = math.inf
    fire_time: List[List[float]] = [[INF] * c for _ in range(r)]
    pq: list[Tuple[float, int, int]] = []  # (time, x, y)

    # Initialize queue with initial fire sources
    for i in range(r):
        for j in range(c):
            if grid[i][j] == 'F':
                fire_time[i][j] = 0
                heappush(pq, (0, i, j))

    def step_cost(dx: int, dy: int) -> int:
        if wind_vec is None:
            return 1
        wx, wy = wind_vec
        if (dx, dy) == (wx, wy):
            return 1
        if (dx, dy) == (-wx, -wy):
            return 3  # against the wind (slowest)
        return 2  # perpendicular

    while pq:
        t, x, y = heappop(pq)
        if t > fire_time[x][y]:
            continue
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < r and 0 <= ny < c and grid[nx][ny] != '#':
                nt = t + step_cost(dx, dy)
                if nt < fire_time[nx][ny]:
                    fire_time[nx][ny] = nt
                    heappush(pq, (nt, nx, ny))

    # Convert math.inf back to -1 for consistency
    return [[-1 if t is INF else int(t) for t in row] for row in fire_time]


def earliest_escape_time(grid: List[List[str]], start: Coord, fire_time: List[List[int]]) -> int | None:
    """Computes the minimum time to reach any border cell before the fire.

    Returns the number of minutes needed to escape or None if impossible.
    """
    r, c = len(grid), len(grid[0])
    visited = [[False] * c for _ in range(r)]
    q: deque[Tuple[int, int, int]] = deque()  # (x, y, time)
    x0, y0 = start
    visited[x0][y0] = True
    q.append((x0, y0, 0))

    while q:
        x, y, t = q.popleft()
        # Check if at border -> escape
        if x == 0 or x == r - 1 or y == 0 or y == c - 1:
            return t + 1  # escape takes 1 more minute to move out

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            nt = t + 1
            if 0 <= nx < r and 0 <= ny < c and not visited[nx][ny]:
                if grid[nx][ny] == '#':
                    continue  # wall
                # Check fire timing: can enter only if either never burns or burns after arrival
                if fire_time[nx][ny] != -1 and fire_time[nx][ny] <= nt:
                    continue
                visited[nx][ny] = True
                q.append((nx, ny, nt))
    return None


def print_fire_time(fire_time: List[List[int]]):
    for row in fire_time:
        print(' '.join(f"{t:2d}" for t in row))


def main():
    grid, start, wind_vec = read_grid_from_stdin()
    fire_time = compute_fire_time(grid, wind_vec)

    # Uncomment next line to debug fire spread times
    # print_fire_time(fire_time)

    result = earliest_escape_time(grid, start, fire_time)
    if result is None:
        print("IMPOSSIBLE")
    else:
        print(result)

if __name__ == "__main__":
    main()