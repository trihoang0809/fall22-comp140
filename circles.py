"""
Code to calculate the circle that passes through three given points.

Fill in each function with your code (including fixing the return
statement).
"""

import math
import comp140_module1 as circles

def distance(point0x, point0y, point1x, point1y):
    """
    Computes the distance between two points.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: a float that is the distance between the two points
    """
    return math.sqrt((point0x - point1x)**2 + (point0y - point1y)**2)

print(distance(3, 2, 4, 1))

def midpoint(point0x, point0y, point1x, point1y):
    """
    Computes the midpoint between two points.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: two floats that are the x- and y-coordinates of the midpoint
    """
    midpoint_x = point0x + ((point1x - point0x) / 2)
    midpoint_y = point0y + ((point1y - point0y) / 2)
    return midpoint_x, midpoint_y

print(midpoint(1, 2, 2, 3))

def slope(point0x, point0y, point1x, point1y):
    """
    Computes the slope of the line that connects two given points.

    The x-values of the two points, point0x and poin1x, must be different.

    inputs:
        -point0x: a float representing the x-coordinate of the first point.
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point.
        -point1y: a float representing the y-coordinate of the second point

    returns: a float that is the slope between the points
    """
    return (point1y - point0y) / (point1x - point0x)

print(slope(2, 3, 4, 5))

def perp(lineslope):
    """
    Computes the slope of a line perpendicular to a given slope.

    input:
        -lineslope: a float representing the slope of a line.
                    Must be non-zero

    returns: a float that is the perpendicular slope
    """
    return (-1) / lineslope

def intersect(slope0, point0x, point0y, slope1, point1x, point1y):
    """
    Computes the intersection point of two lines.

    The two slopes, slope0 and slope1, must be different.

    inputs:
        -slope0: a float representing the slope of the first line.
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -slope1: a float representing the slope of the second line.
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: two floats that are the x- and y-coordinates of the intersection
    point
    """
    intersect_x = (
        (slope0 * point0x) - (slope1 * point1x) + (point1y - point0y)
                  ) / (slope0 - slope1)
    intersect_y = slope0 * (intersect_x - point0x) + point0y
    return intersect_x, intersect_y

def make_circle(point0x, point0y, point1x, point1y, point2x, point2y):
    """
    Computes the center and radius of a circle that passes through
    thre given points.

    The points must not be co-linear and no two points can have the
    same x or y values.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point
        -point2x: a float representing the x-coordinate of the third point
        -point2y: a float representing the y-coordinate of the third point

    returns: three floats that are the x- and y-coordinates of the center
    and the radius
    """
# Finding the x and y coordinates of the midpoints of the two lines
    midpoint0x, midpoint0y = midpoint(point0x, point0y, point1x, point1y)
    midpoint1x, midpoint1y = midpoint(point0x, point0y, point2x, point2y)
#Finding the slopes of the two lines
    slope0 = slope(point0x, point0y, point1x, point1y)
    slope1 = slope(point0x, point0y, point2x, point2y)
#Finding the slopes of 2 lines perpendicular to the initial 2 lines
    perp0 = perp(slope0)
    perp1 = perp(slope1)
#The x and y coordinate of the center of the circle is the x and y intercept of 
#two lines with the slopes perp1 and perp2 and pass midpoint 1 and midpoint2
    x_center, y_center = intersect(perp0, midpoint0x, midpoint0y, perp1, midpoint1x, midpoint1y)
#The radius of the circle is equal to the distance from the center of the circle
#to one of the three initial points
    radius = distance(point0x, point0y, x_center, y_center)
    return x_center, y_center, radius

# Run GUI - uncomment the line below after you have
#          implemented make_circle
circles.start(make_circle)
