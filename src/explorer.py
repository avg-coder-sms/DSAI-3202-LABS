import time
import pygame
from typing import Tuple, List, Optional
from collections import deque
from .constants import BLUE, WHITE, CELL_SIZE, WINDOW_SIZE
import heapq

# NEW CLASS: Node used for A* algorithm
class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0  # Cost to get here
        self.h = 0  # Estimated cost to goal
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f

class Explorer:
    def __init__(self, maze, visualize: bool = False):
        self.maze = maze
        self.x, self.y = maze.start_pos
        self.direction = (1, 0)  # Start facing right
        self.moves = []
        self.start_time = None
        self.end_time = None
        self.visualize = visualize
        self.move_history = deque(maxlen=3)  # For simple loop detection
        self.backtracking = False
        self.backtrack_path = []
        self.backtrack_count = 0  # Count number of backtrack operations

        # MODIFIED: Track how many times each cell is visited
        self.visited_counts = {}
        self._update_visited(self.x, self.y)

        if visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Maze Explorer - Automated Solving")
            self.clock = pygame.time.Clock()

    def _update_visited(self, x, y):
        pos = (x, y)
        self.visited_counts[pos] = self.visited_counts.get(pos, 0) + 1

    def can_move(self, x, y) -> bool:
        return (0 <= x < self.maze.width and 
                0 <= y < self.maze.height and 
                self.maze.grid[y][x] == 0)

    # NEW: Manhattan distance heuristic for A*
    def heuristic(self, x, y, goal_x, goal_y):
        return abs(x - goal_x) + abs(y - goal_y)

    # NEW: A* search algorithm implementation
    def a_star(self):
        open_list = []
        closed_list = set()

        start_node = Node(self.x, self.y)
        start_node.g = 0
        start_node.h = self.heuristic(self.x, self.y, self.maze.end_pos[0], self.maze.end_pos[1])
        start_node.f = start_node.g + start_node.h

        heapq.heappush(open_list, start_node)

        while open_list:
            current_node = heapq.heappop(open_list)
            closed_list.add((current_node.x, current_node.y))

            if (current_node.x, current_node.y) == self.maze.end_pos:
                # PATH FOUND: Trace back the path using parent pointers
                path = []
                while current_node:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return path[::-1]  # Return reversed path from start to end

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = current_node.x + dx, current_node.y + dy

                if not self.can_move(new_x, new_y) or (new_x, new_y) in closed_list:
                    continue

                neighbor = Node(new_x, new_y, current_node)
                neighbor.g = current_node.g + 1
                neighbor.h = self.heuristic(new_x, new_y, self.maze.end_pos[0], self.maze.end_pos[1])
                neighbor.f = neighbor.g + neighbor.h

                # OPTIMIZED: Only add if this path is better than existing one
                if all(neighbor.f < node.f for node in open_list if (node.x, node.y) == (new_x, new_y)):
                    heapq.heappush(open_list, neighbor)

        return None  # No path found

    # NEW: Follow the computed path
    def move_to(self, path: List[Tuple[int, int]]):
        for (x, y) in path:
            self.x, self.y = x, y
            self.moves.append((self.x, self.y))
            self._update_visited(self.x, self.y)
            if self.visualize:
                self.draw_state()

    def draw_state(self):
        self.screen.fill(WHITE)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (x * CELL_SIZE, y * CELL_SIZE,
                                      CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.maze.start_pos[0] * CELL_SIZE,
                          self.maze.start_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.maze.end_pos[0] * CELL_SIZE,
                          self.maze.end_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLUE,
                         (self.x * CELL_SIZE, self.y * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        self.clock.tick(30)

    def print_statistics(self, time_taken: float):
        print("\n=== Maze Exploration Statistics ===")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Total moves made: {len(self.moves)}")
        print(f"Number of backtrack operations: {self.backtrack_count}")
        print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
        print("==================================\n")

    # MODIFIED: New solve function that integrates A* path and tracking
    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        self.start_time = time.time()
        visited = set()
        visited.add((self.x, self.y))
        if self.visualize:
            self.draw_state()

        path = self.a_star()  # Use A* to find optimal path

        if path:
            self.move_to(path)  # Traverse the path using new move_to()

        self.end_time = time.time()
        time_taken = self.end_time - self.start_time
        if self.visualize:
            pygame.time.wait(2000)
            pygame.quit()

        self.print_statistics(time_taken)
        return time_taken, self.moves
