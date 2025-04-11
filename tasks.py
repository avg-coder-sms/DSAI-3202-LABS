# tasks.py

from celery import Celery
from src.maze import create_maze
from src.explorer import Explorer

# Set up Celery app (default RabbitMQ broker and RPC backend)
app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='rpc://')

@app.task
def run_explorer(width, height, maze_type, visualize=False):
    """
    Task to run a maze explorer and return performance metrics.
    """
    maze = create_maze(width, height, maze_type)
    explorer = Explorer(maze, visualize=visualize)
    time_taken, moves = explorer.solve()
    
    return {
        'time_taken': time_taken,
        'moves': len(moves),
        'backtracks': explorer.backtrack_count  # Ensure Explorer tracks backtracks
    }
