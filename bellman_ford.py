from maze_generator import Maze
import time
import psutil

explored_nodes = set()

def bellman_ford(maze):
    # Initialize distances and predecessors
    node_count = maze.length ** 2
    distances = {node: float('inf') for node in maze.nodes}
    predecessors = {node: None for node in maze.nodes}
    start_node = maze.nodes[node_count - 1]  # Bottom-right node
    end_node = maze.nodes[0]  # Top-left node

    distances[start_node] = 0

    # Relax edges |V| - 1 times
    for _ in range(node_count - 1):
        for node in maze.nodes:
            for neighbor in node.adjacencyList:
                explored_nodes.add(node)
                explored_nodes.add(neighbor)
                if distances[node] + 1 < distances[neighbor]:  # Edge weight is assumed to be 1
                    distances[neighbor] = distances[node] + 1
                    predecessors[neighbor] = node

    # Reconstruct the path
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = predecessors[current_node]

    path.reverse()  # Reverse to get the path from start to end
    return path

def main(maze):
    # Record the initial memory usage
    process = psutil.Process()
    initial_memory = process.memory_info().rss

    # Start the timer
    start_time = time.time()

    path = bellman_ford(maze)

    # Record the final memory usage
    final_memory = process.memory_info().rss  # Resident Set Size in bytes

    # Calculate memory usage difference
    memory = (final_memory - initial_memory) / 1024 / 1024  # Convert to MB

    # Stop the timer
    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "path": path,
        "node_count": maze.length ** 2,
        "explored_nodes": len(explored_nodes),
        "time": execution_time,
        "memory": memory,
    }

if __name__ == "__main__":
    maze_length = int(input("Enter the length of the maze (10, 20, 50, or 100): "))
    maze = Maze(maze_length)
    result = main(maze)
    print(result)
