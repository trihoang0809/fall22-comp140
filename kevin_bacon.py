"""
The Kevin Bacon Game.

Replace "pass" with your code.
"""

import simpleplot
import comp140_module4 as movies
from collections import defaultdict

class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """
        Initialize the queue.
        """
        self._queue = []

    def __len__(self):
        """
        Returns: an integer representing the number of items in the queue.
        """
        return len(self._queue)

    def __str__(self):
        """
        Returns: a string representation of the queue.
        """
        string_queue = ""
        for item in self._queue:
            string_queue.join(item)
        return string_queue
            

    def push(self, item):
        """
        Add item to the queue.

        input:
            - item: any data type that's valid in a list
        """
        self._queue.append(item)

    def pop(self):
        """
        Remove the least recently added item.

        Assumes that there is at least one element in the queue.  It
        is an error if there is not.  You do not need to check for
        this condition.

        Returns: the least recently added item.
        """
        return self._queue.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        copy_queue = self._queue.copy()
        for item in copy_queue:
            self._queue.remove(item)


def bfs(graph, start_node):
    """
    Performs a breadth-first search on graph starting at the
    start_node.

    inputs:
        - graph: a graph object
        - start_node: a node in graph representing the start node

    Returns: a two-element tuple containing a dictionary
    associating each visited node with the order in which it
    was visited and a dictionary associating each visited node
    with its parent node.
    """
#implementing the BFS recipe step by step    
    queue = Queue()
    dist = {}
    parent = {}
    for node in graph.nodes():
        dist[node] = float("inf")
        parent[node] = None
    dist[start_node] = 0
    queue.push(start_node)
    while len(queue) > 0:
        node = queue.pop()
        for nbr in graph.get_neighbors(node):
            if dist[nbr] == float("inf"):
                dist[nbr] = dist[node] + 1
                parent[nbr] = node
                queue.push(nbr)
    return (dist, parent)

def distance_histogram(graph, node):
    """
    Computes the distance between the given node and all other
    nodes in that graph and creates a histogram of those distances.

    inputs:
        - graph: a graph object
        - node: a node in graph

    returns: a dictionary mapping each distance with the number of
    nodes that are that distance from node.
    """
    dis_his = defaultdict(int)
#create a list version of the bfs's function's output so it is iterable
    bfs_output = list(bfs(graph, node))
    for dictionary in bfs_output:
#checking: if 0 is a value in one of two dictionaries in the output of
#the bfs function -> that is the dist dictionary
        if 0 in dictionary.values():
#iterate through the values of the dist dictionary, with each value
#being the key of the dis_his dictionary
            for value in dictionary.values():
                dis_his[value] += 1
    return dis_his
    
def find_path(graph, start_person, end_person, parents):
    """
    Computes the path from start_person to end_person in the graph.

    inputs:
        - graph: a graph oject with edges representing the connections between people
        - start_person: a node in graph representing the starting node
        - end_person: a node in graph representing the ending node
        - parents: a dictionary representing the parents in the graph

    returns a list of tuples of the path in the form:
        [(actor1, {movie1a, ...}), (actor2, {movie2a, ...}), ...]
    """
#idea: trace back from the end_person until the start_person is found
    current_node = end_person
    path = []
#loop until start_person is reached
    while current_node != start_person:
        current_parent = parents[current_node]
        if parents[current_node] == None:
            return []
#prepend to the path the step
        path.insert(0, (current_parent, graph.get_attrs(current_node, current_parent)))
        current_node = current_parent
    path.append((end_person, set()))
    return path

def play_kevin_bacon_game(graph, start_person, end_people):
    """
    Play the "Kevin Bacon Game" on the actors in the given
    graph.

    inputs:
        - graph: a a graph oject with edges representing the connections between people
        - start_person: a node in graph representing the node from which the search will start
        - end_people: a list of nodes in graph to which the search will be performed

    Prints the results out.
    """
    bfs_output = list(bfs(graph, start_person))
    for dictionary in bfs_output:
#checking: if 0 is a value in one of two dictionaries in the output of
#the bfs function -> that is the dist dictionary
        if 0 not in dictionary.values():
            parents = dictionary
    for end_person in end_people:
        path = find_path(graph, start_person, end_person, parents)
        movies.print_path(path)
        

def run():
    """
    Load a graph and play the Kevin Bacon Game.
    """
    graph5000 = movies.load_graph('subgraph5000')

    if len(graph5000.nodes()) > 0:
        # You can/should use smaller graphs and other actors while
        # developing and testing your code.
        play_kevin_bacon_game(graph5000, 'Kevin Bacon',
            ['Amy Adams', 'Andrew Garfield', 'Anne Hathaway', 'Barack Obama', \
             'Benedict Cumberbatch', 'Chris Pine', 'Daniel Radcliffe', \
             'Jennifer Aniston', 'Joseph Gordon-Levitt', 'Morgan Freeman', \
             'Sandra Bullock', 'Tina Fey'])

        # Plot distance histograms
        for person in ['Kevin Bacon', 'Stephanie Fratus']:
            hist = distance_histogram(graph5000, person)
            simpleplot.plot_bars(person, 400, 300, 'Distance', \
                'Frequency', [hist], ["distance frequency"])

# Uncomment the call to run below when you have completed your code.

# run()
