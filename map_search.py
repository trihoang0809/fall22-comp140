"""
Map Search
"""

import comp140_module7 as maps

class Queue:
    """
    A simple implementation of a FIFO queue.
    """
    def __init__(self):
        """
        Initialize the queue.
        """
        self._items = []
        
    def __len__(self):
        """
        Returns: an integer representing the number of items in the 
        queue.
        """
        return len(self._items)
    
    def __str__(self):
        """
        Returns: a string representation of the current state of the
        queue.
        """
        return "Current state: " + str(self._items)
        
    def push(self, item):
        """
        Add item to the queue.

        input:
            - item: any data type that's valid in a list
        """
        self._items.append(item)
        
    def pop(self):
        """
        Remove the least recently added item.

        Assumes that there is at least one element in the queue.

        Returns: the least recently added item.
        """
        return self._items.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []

class Stack:
    """
    A simple implementation of a LIFO stack.
    """
    def __init__(self):
        """
        Initialize the stack.
        """
        self._items = []
        
    def __len__(self):
        """
        Returns: an integer representing the number of items in the 
        stack.
        """
        return len(self._items)
    
    def __str__(self):
        """
        Returns: a string representation of the current state of the
        stack.
        """
        return "Current state: " + str(self._items)
        
    def push(self, item):
        """
        Add item to the stack.

        input:
            - item: any data type that's valid in a list
        """
        self._items.append(item)
        
    def pop(self):
        """
        Remove the most recently added item.

        Assumes that there is at least one element in the queue.

        Returns: the stack recently added item.
        """
        return self._items.pop()

    def clear(self):
        """
        Remove all items from the stack.
        """
        self._items = []


def bfs_dfs(graph, rac_class, start_node, end_node):
    """
    Performs a breadth-first search or a depth-first search on graph
    starting at the start_node. The rac_class should either be a
    Queue class or a Stack class to select BFS or DFS.

    Completes when end_node is found or entire graph has been
    searched.

    inputs:
        - graph: a directed Graph object representing a street map
        - rac_class: a restricted access container (Queue or Stack) class to
          use for the search
        - start_node: a node in graph representing the start
        - end_node: a node in graph representing the end

    Returns: a dictionary associating each visited node with its parent
    node.
    """
    rac = rac_class()
    parent = {}
    for graph_node in graph.nodes():
        parent[graph_node] = None
    rac.push(start_node)
    while len(rac) > 0:
        node = rac.pop()
        for nbr in graph.get_neighbors(node):
#check if nbr has been gone through or not
            if parent[nbr] == None:
                parent[nbr] = node
                rac.push(nbr)
                if nbr == end_node:
                    return parent               
    return parent
    
def dfs(graph, start_node, end_node, parent):
    """
    Performs a recursive depth-first search on graph starting at the
    start_node.

    Completes when end_node is found or entire graph has been
    searched.

    inputs:
        - graph: a directed Graph object representing a street map
        - start_node: a node in graph representing the start
        - end_node: a node in graph representing the end
        - parent: a dictionary that initially has one entry associating
                  the original start_node with None

    Modifies the input parent dictionary to associate each visited node
    with its parent node
    """
#implement the recipe for the dfs recursive function
#check if the neighbors of start_node are already in parent or not
    checked = True
    for nbr in graph.get_neighbors(start_node):
        if nbr not in parent.keys():
            checked = False
#base case: if all neighbors of start_node are already in parent    
    if checked == True:
        return
#recursive case    
    else:
        for nbr in graph.get_neighbors(start_node):
            if nbr not in parent.keys():
                parent[nbr] = start_node
                if nbr == end_node:
                    return
                dfs(graph, nbr, end_node, parent)

def lowest_f(graph, openset, g_cost_dict, straight_line_distance, end_node):
    """
    This function returns the node with the lowest f-cost in the open set in A* search.
    This function serves as a helper function for the astar function.
    Inputs:
        - graph: a directed Graph object representing a street map
        - openset: a set representing the nodes to be traversed
        - g_cost_dict: a dictionary which maps nodes to their g_costs
        - straight_line_distance: a function which takes two nodes and
                         a graph and returns the straight line distance 
                         between two nodes
        - end_node: a node in graph representing the end
    Output: the node with the lowest f-cost in the openset
    """    
    f_cost = {}
    curr_node = None
    for node in openset: 
        f_cost[node] = g_cost_dict[node] + straight_line_distance(node, end_node, graph)
        for key, value in f_cost.items():
            if value == min(f_cost.values()):
                curr_node = key
    return curr_node


def astar(graph, start_node, end_node,
          edge_distance, straight_line_distance):
    """
    Performs an A* search on graph starting at start_node.

    Completes when end_node is found or entire graph has been
    searched.

    inputs:
        - graph: a directed Graph object representing a street map
        - start_node: a node in graph representing the start
        - end_node: a node in graph representing the end
        - edge_distance: a function which takes two nodes and a graph
                         and returns the actual distance between two
                         neighboring nodes
        - straight_line_distance: a function which takes two nodes and
                         a graph and returns the straight line distance 
                         between two nodes

    Returns: a dictionary associating each visited node with its parent
    node.
    """
    parent = {start_node: None}
#create a dictionary that maps the nodes to its g-cost    
    g_cost_dict = {start_node: 0}
    
#create the open set and the closed set    
    openset = set()
    closedset = set()    
    openset.add(start_node)
    cur_node = None 
    
    while len(openset) > 0:
#find the node with the lowest f cost in the openset        
        cur_node = lowest_f(graph, openset, g_cost_dict, straight_line_distance, end_node)
#remove current node from the open set and add it to the closed set        
        openset.remove(cur_node)
        closedset.add(cur_node)
#look at the current node's neighbors
        for nbr in graph.get_neighbors(cur_node):
            if nbr not in closedset:
#if the nbr is not in the open set yet, add it                
                if nbr not in openset:
                    parent[nbr] = cur_node
                    openset.add(nbr)
                    g_cost_dict[nbr] = g_cost_dict[cur_node] + edge_distance(cur_node, nbr, graph)
                elif nbr in openset:
                    nbr_g_cost = g_cost_dict[cur_node] + edge_distance(cur_node, nbr, graph)
                    if nbr_g_cost < g_cost_dict[nbr]:
                        g_cost_dict[nbr] = nbr_g_cost
                        parent[nbr] = cur_node
    return parent

# You can replace functions/classes you have not yet implemented with
# None in the call to "maps.start" below and the other elements will
# work.

maps.start(bfs_dfs, Queue, Stack, dfs, astar)
