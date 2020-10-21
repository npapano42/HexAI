from __future__ import annotations


class DisjointSet:
    """
    DisjointSet is an implementation of the Disjoint Set data structure, customized to the work with the game board.
    """

    def __init__(self, board_size: int):
        """
        Constructs a DisjointSet object, given an input board size

        Parameters:
            board_size : int
                the size of the board
        """
        self.sets = set()
        self.nodes = []
        for row in range(board_size):
            self.nodes.append([])
            for col in range(board_size):
                next_node = Node((row, col))
                self.nodes[row].append(next_node)
                self.sets.add(next_node)

    def union_sets(self, v1: Node, v2: Node):
        """
        Performs the union operation to combine nodes from two sets. Will do nothing on nodes in the same set.
        Applies both path compression and union by size optimizations

        Parameters:
            v1 : Node
                The first node to union
            v2 : Node
                The second node to union
        """
        v1_parent = self.get_head(v1)
        v2_parent = self.get_head(v2)
        if v1_parent is not v2_parent:
            if v1_parent.size > v2_parent.size:
                v1_parent.add_child(v2_parent)
                v1.size += v2.size
            else:
                v2_parent.add_child(v1_parent)
                v2.size += v1.size

    def get_node(self, x, y) -> Node:
        """
        Finds a node object based on a given (x,y) coordinate

        Parameters:
            x : int
                the x coordinate of the location for the node
            y : int
                the y coordinate of the location for the node

        Returns:
            The node object with the given (x,y) coordinates
        """
        return self.nodes[x][y]

    def get_head(self, v: Node) -> Node:
        """
        Traverses up v's parents and returns the head of the set that contains v

        Parameters:
            v : Node
                A node in a disjoint set

        Returns:
            The head node of the set v is in
        """
        if v.parent is None:
            return v
        v.parent = self.get_head(v.parent)
        return v.parent

    def visualize(self):
        """
        Provides a nice-looking console output for the current status of the data structure.
        Heads of sets are marked with >, and children of that node are tabbed over
        Ex.
        >(1, 1)
	        (0, 1)
	            (0, 2)
	        (0, 0)
	    Shows that there is 1 set, (1, 1) is the head, with (0, 1) and (0, 0) as children, and (0, 1) has (0, 2) as a child
        """
        for node in self.sets:
            print(">", end="")
            node.print("")
        print("\n")


class Node:
    """
    Internal Node class to generalize DisjointSet operations and wrap data
    """

    def __init__(self, data, parent: Node = None, children: list = None):
        """
        Creates a Node by wrapping the data parameter

        Parameters:
            data : Any
                Data to store in the node
            parent : Node
                The node that the current in-construction node should be the child of
            children : list
                A list of nodes that hte in-construction node should be the parent of
        """

        if children is None:
            children = []
        self.data = data
        self.parent = parent
        self.children = children
        self.size = 1

    def add_child(self, child: Node):
        """
        Connects a child to the current node, adjusting it's parent reference as well

        Parameters:
            child : Node
                The new incoming child node
        """
        child.parent = self
        self.children.append(child)

    def __eq__(self, other):
        """
        Basic overwritten equals implementation, checking equality of data

        Parameters:
            other : Node
                the Node to be compared to

        Returns:
            True if data is equal, false otherwise
        """
        return self.data == other.data

    def __hash__(self):
        """
        Basic overwritten hash implementation for set operations to function

        Returns:
            the result of calling hash() on the data
        """
        return hash(self.data)

    def print(self, indent):
        """
        Prints a node to the console given an indent size.
        Exists as a helper to facilitate the visualization of DisjointSet

        Parameters:
            indent : str
                the string to be indented over (a series of tabs)
        """
        print(indent + str(self.data))
        for child in self.children:
            child.print(indent + "\t")
