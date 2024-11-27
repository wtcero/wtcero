import random
import math

class Node:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.parent_i = self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = self.col + self.row
        self.adjacencyList = set()
    
class Edge:
    def __init__(self, head, tail):
        self.connectedNodes = frozenset([head, tail])
        self.weight = 1
    
    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.connectedNodes == other.connectedNodes
        return False

    def __hash__(self):
        return hash(frozenset(self.connectedNodes))
    
class Maze:
    
    def __init__(self, length):
        self.length = length
        self.nodesPosition = [None for _ in range(self.length)]
        self.nodes = list()
        self.edges = set()
        self.walls = set()
        self.adjacencyMatrix = [[math.inf] * (length ** 2) for k in range(length ** 2)]
        self.nodeToIndex = {}
        
        
        # Generate all the nodes
        index = 0
        for row in range(length):
            self.nodesPosition[row] = [None for _ in range(self.length)]
            for col in range(length):
                node = Node(col, row)
                self.nodesPosition[row][col] = node
                self.nodeToIndex[node] = index
                self.nodes.append(node)
                index += 1
                
        # Generate all possible edges
        for row in range(length):
            for col in range(length):
                if col < length - 1:
                    RightEdge = Edge(self.nodesPosition[row][col], self.nodesPosition[row][col+1])
                    self.edges.add(RightEdge)
                if row < length - 1:
                    DownEdge = Edge(self.nodesPosition[row][col], self.nodesPosition[row+1][col])
                    self.edges.add(DownEdge)

        # Shuffle edges to mimic the random nature of Kruskal's algorithm
        self.edges = list(self.edges)
        random.shuffle(self.edges)
        
        # Initialize the adjacencyMatrix
        for i in range(length ** 2):
            self.adjacencyMatrix[i][i] = 0
        
        self.updateToMSTEdges()
        
        # self.printGraph()
        
        # for row in self.adjacencyMatrix:
        #     print(row)
        
        

    def find(self, parent, node):
        if parent[node] != node:
            parent[node] = self.find(parent, parent[node])
        return parent[node]
    
    def union(self, parent, rank, node1, node2):
        root1 = self.find(parent, node1)
        root2 = self.find(parent, node2)
        
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    def generateMST(self):
        parent = {}
        rank = {}

        # Initially, each node is its own parent
        for row in self.nodesPosition:
            for node in row:
                parent[node] = node
                rank[node] = 0
        
        # Add edges until there are enough edges to form a connected graph (MST)
        mst_edges = set()
        
        for edge in self.edges:
            node1, node2 = edge.connectedNodes

            root1 = self.find(parent, node1)
            root2 = self.find(parent, node2)

            # If no cycle is formed, add the edge to the MST
            if root1 != root2:
                mst_edges.add(edge)
                self.union(parent, rank, root1, root2)
                node1.adjacencyList.add(node2)
                node2.adjacencyList.add(node1)

        # Now mst_edges contains the edges of the maze (no cycles)
        # These are the edges that remain in the maze

        return mst_edges
    
    def printGraph(self):
        for row in range(self.length):
            for col in range(self.length):
                print("x", end="")
                if col < self.length - 1:
                    edge = Edge(self.nodesPosition[row][col], self.nodesPosition[row][col+1])
                    if edge in self.edges:
                        print(" <-> ", end="")
                    else:
                        print("     ", end="")
            print()

            for col in range(self.length):
                if row < self.length - 1:
                    edge = Edge(self.nodesPosition[row][col], self.nodesPosition[row+1][col])
                    if edge in self.edges:
                        print("|     ", end="")
                    else:
                        print("      ", end="")
            print()
        
        for row in self.nodesPosition:
            for node in row:
                node_position = [node.row, node.col]
                # print(node_position, end=" -> {")
                for neighbor in node.adjacencyList:
                    neighborPosition = [neighbor.row, neighbor.col]
                    # print(neighborPosition, end=", ")
                # print("}")
            
    def updateToMSTEdges(self):
        mstEdges = self.generateMST()
        self.edges.clear()
        for edge in mstEdges:
            connectedNodes = list(edge.connectedNodes)
            nodePosition = [connectedNodes[0].row, connectedNodes[0].col]
            neighborPosition = [connectedNodes[1].row, connectedNodes[1].col]
            # print(f'{nodePosition} -> {neighborPosition}')
            self.edges.append(edge)
            index0 = self.nodeToIndex[connectedNodes[0]]
            index1 = self.nodeToIndex[connectedNodes[1]]
            # print(f'Index 0: {index0} | Index 1: {index1}')
            
            self.adjacencyMatrix[index0][index1] = 1
            self.adjacencyMatrix[index1][index0] = 1
            
# maze = Maze(3)