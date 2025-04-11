# main.py
import argparse
from tasks import run_explorer
from time import time

def log_and_print(log_file, message):
    print(message)
    log_file.write(message + '\n')

def main():
    parser = argparse.ArgumentParser(description="Parallel Maze Explorer")
    parser.add_argument("--type", choices=["random", "static"], default="random")
    parser.add_argument("--width", type=int, default=30)
    parser.add_argument("--height", type=int, default=30)
    parser.add_argument("--explorers", type=int, default=5,
                        help="Number of explorers to run in parallel")
    args = parser.parse_args()

    with open("explorer_log.txt", "w") as log_file:
        log_and_print(log_file, f"Spawning {args.explorers} parallel explorers...")
        task_results = []

        start_time = time()
        for _ in range(args.explorers):
            task = run_explorer.delay(args.width, args.height, args.type)
            task_results.append(task)

        results = [task.get(timeout=120) for task in task_results]
        total_time = time() - start_time

        log_and_print(log_file, "\n=== Results from all explorers ===")
        for idx, res in enumerate(results):
            log_and_print(log_file, f"Explorer {idx+1}: Time = {res['time_taken']:.2f}s, "
                                    f"Moves = {res['moves']}, Backtracks = {res['backtracks']}")

        best = sorted(results, key=lambda r: (r['time_taken'], r['moves']))[0]
        log_and_print(log_file, "\n🏆 Best Explorer Performance:")
        log_and_print(log_file, f"Time: {best['time_taken']:.2f}s, Moves: {best['moves']}, Backtracks: {best['backtracks']}")
        log_and_print(log_file, f"Total parallel runtime: {total_time:.2f}s")

if __name__ == "__main__":
    main()
