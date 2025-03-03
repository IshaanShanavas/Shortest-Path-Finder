import curses
from curses import wrapper
import heapq
import time

def manhattan_distance(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

maze = [
    list("########################################"),
    list("#O       #                #         # X#"),
    list("### ##### ### ### ######### ###### ## #"),
    list("#   #   #   #                   #     #"),
    list("# ### ### ### ### ### # ### ### # ### #"),
    list("# #   #   #   # # # #   #   # # #     #"),
    list("# # ### ### # # # # ####### # ####### #"),
    list("# #     # # # # #     #     #   #     #"),
    list("# ##### # # # ####### # ####### # #####"),
    list("#           #       # #       #       #"),
    list("########################################"),
]

def print_maze(maze, stdscr, path=[]):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "X", curses.color_pair(2))  # Red path
            else:
                stdscr.addstr(i, j * 2, value, curses.color_pair(1))  # Blue walls and spaces

def find_position(maze, symbol):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == symbol:
                return i, j
    return None

def find_neighbors(maze, row, col, visited):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    neighbors = []
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] != "#" and (r, c) not in visited:
            neighbors.append((r, c))
    return neighbors

def find_path(maze, stdscr):
    start = find_position(maze, "O")
    goal = find_position(maze, "X")
    if not start or not goal:
        return
    
    pq = []  # Priority queue
    heapq.heappush(pq, (0, start, [start]))  # (cost, position, path)
    visited = set()
    
    while pq:
        cost, current, path = heapq.heappop(pq)
        row, col = current
        
        stdscr.clear()
        print_maze(maze, stdscr, path)
#        time.sleep(0.000002)
        stdscr.refresh()
        
        if current == goal:
            stdscr.clear()
            print_maze(maze, stdscr, path)
            stdscr.refresh()
            stdscr.getch()  # Wait for keypress before exiting
            return
        
        if current in visited:
            continue
        visited.add(current)
        
        for neighbor in find_neighbors(maze, row, col, visited):
            new_cost = len(path) + manhattan_distance(neighbor, goal)
            heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    find_path(maze, stdscr)

wrapper(main)
