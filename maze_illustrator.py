import turtle
from maze_generator import Maze
# import floyd_warshall
import bellman_ford
import os
import uuid

CELL_SIZE = 30  # size of each cell in pixels
MAZE_SIZE = 50  # length of the maze grid

# # Set up a larger canvas size based on the maze dimensions
CANVAS_WIDTH = MAZE_SIZE * CELL_SIZE + 100  # extra padding for visibility
CANVAS_HEIGHT = MAZE_SIZE * CELL_SIZE + 100

# Initialize Turtle screen with the enlarged canvas
turtle.setup(width=1000, height=1000)

def draw_grid(t, maze_length):
    for row in range(maze_length):
        for col in range(maze_length):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            draw_square(t, x, y)

def draw_square(t, x, y):
    t.penup()
    t.pensize(2)
    t.goto(x, -y)
    t.pendown()
    for _ in range(4):
        t.forward(CELL_SIZE)
        t.right(90)

def mark_cell(t, node, color):
    x, y = (node.col * CELL_SIZE), (node.row * CELL_SIZE)
    t.penup()
    t.goto(x, -y)
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
         t.forward(CELL_SIZE - 2)
         t.right(90)
    t.end_fill()
    row, col = node.row, node.col

    # Calculate the center of the cell
    center_x = col * CELL_SIZE + CELL_SIZE / 2
    center_y = -row * CELL_SIZE - CELL_SIZE / 2

    # Move turtle to the center of the cell
    t.penup()
    t.goto(center_x, center_y - CELL_SIZE / 6)  # Adjust for circle's bottom
    t.pendown()

    # Draw the circle
    t.fillcolor(color)
    t.begin_fill()
    t.circle(CELL_SIZE / 6)  # Radius is 1/6th of the cell size
    t.end_fill()
    

def remove_wall(t, node1, node2):
    x1, y1 = node1.col * CELL_SIZE, node1.row * CELL_SIZE
    x2, y2 = node2.col * CELL_SIZE, node2.row * CELL_SIZE
    t.pencolor("white")
    t.pensize(2)

    t.penup()
    if x1 == x2:  # Horizontal wall
        x = x1 + 3
        y = max(abs(y1), abs(y2))
        t.goto(x, -y)
        t.setheading(0)
    elif y1 == y2:  # Vertical wall
        x = max(x1, x2)
        y = y1 + 3
        t.goto(x, -y)
        t.setheading(270)
    
    t.pendown()
    t.forward(CELL_SIZE - 5)
    t.pencolor("black")

def create_entry_exit(t, maze):
    # Remove left wall of top-left node (entry)
    t.pensize(2)
    t.pencolor("white")
    t.penup()
    t.goto(0, 0)
    t.setheading(270)
    t.pendown()
    t.forward(CELL_SIZE)

    # Remove right wall of bottom-left node (exit)
    t.penup()
    t.goto((maze.length) * CELL_SIZE, -(maze.length - 1) * CELL_SIZE)
    t.setheading(270)
    t.pendown()
    t.forward(CELL_SIZE-1)

def illustrate_maze(maze, path, algorithm, batch, iteration):
    turtle.setup(width=1000, height=1000)
    t = turtle.Turtle()
    t.speed(0)
    turtle.tracer(0, 0)

    # Shade the solution path in blue
    for node in path:
        Node = maze.nodes[node]
        mark_cell(t, Node, "blue")
        
    draw_grid(t, maze.length)
        
    for edge in maze.edges:
        node1, node2 = edge.connectedNodes
        remove_wall(t, node1, node2)

    # Create entry and exit points
    create_entry_exit(t, maze)
    t.penup()
    
    turtle.update()

    # Folder name
    output_folder = "images"

    # Ensure the folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    temp_filename = f"temp_maze_{uuid.uuid4().hex}.eps"  # Unique EPS filename
    imagename = f"{algorithm}_solution_{batch}_{iteration}.png"
    print(imagename)
    # File name
    filename = os.path.join(output_folder, imagename)
    
    # Save the maze as an image
    ts = t.getscreen()
    ts.getcanvas().postscript(file=temp_filename)
    try:
        from PIL import Image
        img = Image.open(temp_filename)
        img.save(filename, dpi=(1200,1200))
    except ImportError:
        print("PIL library not installed. Could not save maze as an image.")
    finally:
        # Clean up the temporary EPS file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    # turtle.bye()
    del maze
    del path
    return
    # turtle.bye()

# maze = Maze(5)
# returnValues = bellman_ford.main(maze)
# path = returnValues["path"]
# illustrate_maze(maze,path,"bellman_ford", 1, 2)
