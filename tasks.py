from celery import Celery
from src.maze import create_maze
from src.explorer import Explorer

# Set up Celery app (default RabbitMQ broker and RPC backend)
app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='rpc://')

@app.task
def run_explorer(width, height, maze_type, visualize=False, explorer_id=0):
    from src.maze import create_maze
    from src.explorer import Explorer

    maze = create_maze(width, height, maze_type)
    explorer = Explorer(maze, visualize=False)

    time_taken, moves = explorer.solve()
    
    return {
        "explorer_id": explorer_id,
        "time_taken": time_taken,
        "num_moves": len(moves),
        "success": True if moves else False
    }
