"""
Code to implement the game of Spot it!

http://www.blueorangegames.com/spotit/

For each function, replace the return statement with your code.  Add
whatever helper functions you deem necessary.
"""

import comp140_module2 as spotit

def equivalent(point1, point2, mod):
    """
    Determines if the two given points are equivalent in the projective
    geometric space in the finite field with the given modulus.

    Each input point, point1 and point2, must be valid within the
    finite field with the given modulus.

    inputs:
        - point1: a tuple of 3 integers representing the first point
        - point2: a tuple of 3 integers representing the second point
        - mod: an integer representing the modulus

    returns: a boolean indicating whether or not the points are equivalent
    """
    same_point = False
    cross_product = [(point1[1] * point2[2] - point1[2] * point2[1]) % mod,
                     (point1[2] * point2[0] - point1[0] * point2[2]) % mod,
                     (point1[0] * point2[1] - point1[1] * point2[0]) % mod]
    if cross_product == [0, 0, 0]:
        same_point = True
    return same_point

print(equivalent([2, 0, 1], [5, 0, 4], 3))
print(equivalent([4, 3, 3], [1, 5, 2], 4))
        

def incident(point, line, mod):
    """
    Determines if a point lies on a line in the projective
    geometric space in the finite field with the given modulus.

    The inputs point and line must be valid within the finite field
    with the given modulus.

    inputs:
        - point: a tuple of 3 integers representing a point
        - line: a tuple of 3 integers representing a line
        - mod: an integer representing the modulus

    returns: a boolean indicating whether or not the point lies on the line
    """
    point_on_line = False
    if (point[0] * line[0] + point[1] * line[1] + point[2] * line[2]) % mod == 0:
        point_on_line = True
    return point_on_line

print(incident([1, -1, -1], [2, 1, 1], 3))
print(incident([2, 0, 2], [1, 1, 0], 3))

def generate_all_points(mod):
    """
    Generate all unique points in the projective geometric space in
    the finite field with the given modulus.

    inputs:
        - mod: an integer representing the modulus

    Returns: a list of unique points, each is a tuple of 3 elements
    """
    unique_points = []
    all_points = []
    for num1 in range(mod):
        point1 = num1
        for num2 in range(mod):
            point2 = num2
            for num3 in range(mod):
                point3 = num3
                all_points.append([point1, point2, point3])
    for point in all_points:           
        if point != [0, 0, 0]:
            unique = True
            for point2 in unique_points:
                if equivalent(point2, point, mod):
                    unique = False                 
            if unique == True:
                unique_points.append(tuple(point))
    return unique_points

print(generate_all_points(3))

def create_cards(points, lines, mod):
    """
    Create a list of unique cards.

    Each point and line within the inputs, points and lines, must be
    valid within the finite field with the given modulus.

    inputs:
        - points: a list of unique points, each represented as a tuple of 3 integers
        - lines: a list of unique lines, each represented as a tuple of 3 integers
        - mod: an integer representing the modulus

    returns: a list of lists of integers, where each nested list represents a card.
    """
    deck = []
    length = len(points)
    for line in lines:
        valid = []
        for pointidx in range(length):
            point = points[pointidx]
            if incident(point, line, mod):
                valid.append(pointidx)
        deck.append(valid)
    return deck 



def run():
    """
    Create the deck and play the game.
    """
    # Prime modulus
    # Set to 2 or 3 during development
    # Set to 7 for the actual game
    modulus = 7

    # Generate all unique points for the given modulus
    points = generate_all_points(modulus)

    # Lines are the same as points, so make a copy
    lines = points[:]

    # Generate a deck of cards given the points and lines
    deck = create_cards(points, lines, modulus)

    # Run GUI - uncomment the line below after you have implemented
    #           everything and you can play your game.  The GUI does
    #           not work if the modulus is larger than 7.

    spotit.start(deck)

# Uncomment the following line to run your game (once you have
# implemented the run function.)

# run()

