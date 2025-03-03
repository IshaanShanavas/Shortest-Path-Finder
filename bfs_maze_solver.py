import curses
from curses import wrapper
import queue
import time


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

def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
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
    count = 0
    start_pos = find_start(maze, "O")
    if not start_pos:
        return
    
    q = queue.Queue()
    q.put((start_pos, [start_pos]))  # Store position and path
    visited = {start_pos}
    final_path = []
    
    while not q.empty():
        count = count + 1
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        #time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == "X":
            final_path = path  # Store the final path

            break

        for neighbor in find_neighbors(maze, row, col, visited):
            q.put((neighbor, path + [neighbor]))
            visited.add(neighbor)
    
    # Display the final path
    stdscr.clear()
    print("STEPS:", count)
    print_maze(maze, stdscr, final_path)
    stdscr.refresh()
    stdscr.getch()  # Wait for keypress before exiting

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    find_path(maze, stdscr)

wrapper(main)
