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
from typing import List, Tuple

Coord = Tuple[int, int]
DIRECTIONS: List[Coord] = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def read_grid_from_stdin() -> Tuple[List[List[str]], Coord]:
    """Reads a grid from standard input and returns (grid, start_pos)."""
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
    return grid, start


def compute_fire_time(grid: List[List[str]]) -> List[List[int]]:
    """Returns a matrix with the minute each cell catches fire.

    `-1` means the cell never burns.
    """
    r, c = len(grid), len(grid[0])
    fire_time = [[-1] * c for _ in range(r)]
    q: deque[Tuple[int, int]] = deque()

    # Initialize queue with initial fire sources
    for i in range(r):
        for j in range(c):
            if grid[i][j] == 'F':
                q.append((i, j))
                fire_time[i][j] = 0

    while q:
        x, y = q.popleft()
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < r and 0 <= ny < c:
                if grid[nx][ny] != '#' and fire_time[nx][ny] == -1:
                    fire_time[nx][ny] = fire_time[x][y] + 1
                    q.append((nx, ny))
    return fire_time


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
    grid, start = read_grid_from_stdin()
    fire_time = compute_fire_time(grid)

    # Uncomment next line to debug fire spread times
    # print_fire_time(fire_time)

    result = earliest_escape_time(grid, start, fire_time)
    if result is None:
        print("IMPOSSIBLE")
    else:
        print(result)

if __name__ == "__main__":
    main()