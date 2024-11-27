from maze_generator import Maze
import maze_illustrator
# import dijkstra
# import dfs
import bellman_ford
# import floyd_warshall
# import astar
import csv
import multiprocessing
import time


def writeToDataset(returnValues, filename):
    del returnValues["path"]
    with open(filename, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=["node_count", "explored_nodes", "time", "memory"])
        writer.writerow(returnValues)


def callAlgorithms(maze, batch, iteration):
    # dijkstra_returns = dijkstra.main(maze)
    # dijkstra_path = dijkstra_returns["path"]
    # maze_illustrator.illustrate_maze(maze, dijkstra_path, "dijkstra",batch, iteration)
    # writeToDataset(dijkstra_returns, 'dataset_dijkstra.csv')
    
    # dfs_returns = dfs.main(maze)
    # dfs = dfs_returns["path"]
    # maze_illustrator.illustrate_maze(maze, dfs_path, "dfs", batch, iteration)
    # writeToDataset(dfs_returns, 'dataset_dfs.csv')
    
    bellman_ford_returns = bellman_ford.main(maze)
    bellman_ford_path = bellman_ford_returns["path"]
    maze_illustrator.illustrate_maze(maze, bellman_ford_path, "bellman_ford", batch, iteration)
    writeToDataset(bellman_ford_returns, 'dataset_bellman_ford.csv')
    
    #floyd_warshall_returns = floyd_warshall.main(maze)
    #floyd_warshall_path = floyd_warshall_returns["path"]
    #maze_illustrator.illustrate_maze(maze, floyd_warshall_path, "floyd_warshall",batch, iteration)
    #writeToDataset(floyd_warshall_returns, 'dataset_floyd_warshall.csv')
    
    # astar_returns = astar.main(maze)
    # astar_path = astar_returns["path"]
    # maze_illustrator.illustrate_maze(maze, astar_path, "astar",batch, iteration)
    # writeToDataset(astar_returns, 'astar_ford.csv')

def conductTrial(trial_id, maze_length, batch, iteration):
    print(f"Starting trial {trial_id}")
    
    # Create a maze for the trial
    maze = Maze(maze_length)
    
    # Call the algorithms on the maze
    callAlgorithms(maze, batch, iteration)

    print(f"Completed trial {trial_id}")
    time.sleep(5)


def run_trials_parallel(n, maze_length, batch):
    # Create a list of trial IDs
    trials = [(i + 1, maze_length, batch, i + 1) for i in range(n)]
    
    # Use multiprocessing to run trials in parallel
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.starmap(conductTrial, trials)


# Example usage: Run 30 trials with a maze length of 5
if __name__ == "__main__":
    trials = 10
    batchsize = 5
    maze_length = 10
    for i in range(0,trials,batchsize):
        run_trials_parallel(batchsize, maze_length, int(i / batchsize))
        time.sleep(20)