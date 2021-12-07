"""
Quickhull algorithm for finding the convex hull from a list of 2D
planar points.
User can input own parameters, or use default
"""
import math
import timeit
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


"""
Connects two points on the plot with a line
"""
def connectpoints(axs, p1,p2):
    x1, x2 = p1[0], p2[0]
    y1, y2 = p1[1], p2[1]
    axs.plot([x1,x2], [y1,y2],'k-')


"""
Calculates the extrema points on the x axsis
"""
def distance_points(points, range_up, range_low):
    left_p = [range_up,range_up]
    right_p = [range_low,range_low]
    for p in points:
        if p[0] < left_p[0]:
            left_p = p

        if p[0] > right_p[0]:
            right_p = p

    return left_p, right_p

"""
Divides the points into two sets,
the points above and below the extrema points.
"""
def line_sort(points_l, left_mp, right_mp):
    above_arr = []
    below_arr = []
    a = np.array(left_mp)
    b = np.array(right_mp)

    isabove = lambda p, a,b: np.cross(p-a, b-a) < 0
    for i in points_l:
        p1 = np.array(i)

        if p1[0] != a[0] and p1[0] != b[0]:
            if isabove(p1, a, b):
                above_arr.append(i)
            else:
                below_arr.append(i)

    return above_arr, below_arr

"""
Finds the maximum point for the set above in
order to generate a polygon
"""
def max_find(array, range_low):
    y_val = range_low
    max_pnt = 0
    for i in array:
        if i[1] > y_val:
            y_val = i[1]
            max_pnt = i

    return max_pnt

"""
Loops through the point set. The maximum point is added to the convex
hull list. All points conatined in the new hull are expelled. The new list is
sorted again untill all points have been checked.
"""
def above_loop(new_arr, conn_la):
    polygon = Polygon(conn_la)
    while len(new_arr) > 0:
        max_pnt = 0
        distance = 0.0
        index = 0
        for k in new_arr:
            dist = polygon.exterior.distance(Point(k))
            if dist > distance:
                distance = dist
                max_pnt = k
                index = new_arr.index(k)

        if max_pnt == 0:
            return conn_la
        if polygon.contains(Point(tuple(max_pnt))):
            new_arr.pop(index)
        else:
            conn_la.append(max_pnt)
            new_arr.pop(index)
            poly_list = list(map(tuple, conn_la))
            cent=(sum([p[0] for p in poly_list])/len(poly_list),sum([p[1]
                    for p in poly_list])/len(poly_list))
            poly_list.sort(key=lambda p: math.atan2(p[1]-cent[1],p[0]-cent[0]))
            polygon = Polygon(poly_list)

        for k in new_arr:
            if polygon.contains(Point(tuple(k))):
                new_arr.remove(k)

"""
Initially creates the polygon to find the hull.
The extrema points are connected with the maximum point to form the first
hull. If there are no points in the above set, it returns an empty list.
"""
def above_sort(above_arr, left_mp, right_mp, range_low):
    conn_la = []
    if len(above_arr) > 0 :

        conn_la.append(left_mp)
        conn_la.append(right_mp)
        conn_la.append(max_find(above_arr, range_low))

        connection_la = above_loop(above_arr, conn_la)

        return connection_la

    else:
        return conn_la

"""
Finds the minimum point for the below set in
order to generate a polygon
"""
def min_find(array, range_up):
    y_val = range_up
    min_pnt = 0
    for i in array:
        if i[1] < y_val:
            y_val = i[1]
            min_pnt = i

    return min_pnt

"""
Loops through the point set. The minimum point is added to the convex
hull list. All points conatined in the new hull are expelled. The new list is
sorted again untill all points have been checked.
"""
def below_loop(new_arr, conn_lb):
    polygon = Polygon(conn_lb)
    while len(new_arr) > 0:
        max_pnt = 0
        distance = 0.0
        index = 0
        for k in new_arr:
            dist = polygon.exterior.distance(Point(k))
            if dist > distance:
                distance = dist
                max_pnt = k
                index = new_arr.index(k)

        if max_pnt == 0:
            return conn_lb
        if polygon.contains(Point(tuple(max_pnt))):
            new_arr.pop(index)
        else:
            conn_lb.append(max_pnt)
            new_arr.pop(index)
            poly_list = list(map(tuple, conn_lb))
            cent=(sum([p[0] for p in poly_list])/len(poly_list),sum([p[1]
                    for p in poly_list])/len(poly_list))
            poly_list.sort(key=lambda p: math.atan2(p[1]-cent[1],p[0]-cent[0]))
            polygon = Polygon(poly_list)

        for k in new_arr:
            if polygon.contains(Point(tuple(k))):
                new_arr.remove(k)

"""
Initially creates the polygon to find the hull.
The extrema points are connected with the minimum point to form the first
hull. If there are no points in the above set, it returns an empty list.
"""
def below_sort(below_arr, left_mp, right_mp, range_up):
    conn_lb = []
    if len(below_arr) > 0 :
        conn_lb.append(left_mp)
        conn_lb.append(right_mp)
        conn_lb.append(min_find(below_arr, range_up))

        connection_lb = below_loop(below_arr, conn_lb)

        return connection_lb
    else:
        return conn_lb

"""
From the new two sorted sets the hull points are joined together to form the
full convex hull. The result is plotted on a graph.
"""
def hull_sort(above_hull, below_hull, points):

    if len(above_hull) > 0 and len(below_hull) > 0:
        hull = np.concatenate((above_hull, below_hull))
        hull = hull.tolist()
    elif len(above_hull) > 0 and len(below_hull) == 0:
        hull = above_hull
    elif len(below_hull) > 0 and len(above_hull) == 0:
        hull =  below_hull
    else:
        ValueError("Log error")

    seen = set()
    newlist = []
    for item in hull:
        t = tuple(item)
        if t not in seen:
            newlist.append(item)
            seen.add(t)

    poly_list = list(map(tuple, newlist))
    cent=(sum([p[0] for p in poly_list])/len(poly_list),sum([p[1] for p in poly_list])/len(poly_list))
    poly_list.sort(key=lambda p: math.atan2(p[1]-cent[1],p[0]-cent[0]))


    quickhull = np.array(poly_list)
    quickhull = quickhull.tolist()

    fig, (ax1, ax2) = plt.subplots(2, figsize=(15,15))
    fig.suptitle('Quickhull')


    for i in range(0,len(quickhull)-1):
        if i < len(quickhull):
            connectpoints(ax2, quickhull[i],quickhull[i+1])

    connectpoints(ax2, quickhull[0],quickhull[-1])


    data2 = np.array(points)
    x, y = data2.T
    ax1.plot(x, y, 'rd', label =  "Points", markersize=2)
    ax2.plot(x, y, 'rd', markersize=2)
    ax1.legend()


    data1 = np.array(quickhull)
    x, y = data1.T
    ax2.plot(x, y, 'go', label = 'Hull', markersize=4)
    ax2.legend()
    plt.show()

"""
Generates a uniform number of points between the defined ranges
"""
def generate_points(len_points,range_up,range_low):
    point_list = []
    for _ in range(len_points):
        temp = []
        x = np.random.uniform(range_low, range_up)
        y = np.random.uniform(range_low, range_up)
        temp.append(x)
        temp.append(y)
        point_list.append(temp)

    return point_list

"""
Sorts x and y co-ordinates
"""
def sort(x,y):
    array = []
    for i in range(0, len(x)):
        temp = []
        temp.append(x[i])
        temp.append(y[i])
        array.append(temp)
    return array

"""
Creates radius pairs to generate a circle
"""
def rtpairs(r, n):
    for i in range(len(r)):
        for j in range(n[i]):
            yield r[i], j * (2 * np.pi / n[i])


"""
Generates a list of points within a circle boundary
"""
def generate_cirle():
    t_array = []
    r_array = []
    for trn in np.arange(0, 1, 0.01):
        t_array.append(int(trn*100))
        r_array.append(trn)

    x_cord = []
    y_cord = []
    for r, t in rtpairs(t_array, t_array):
        xx = r * np.cos(t)
        yy = r * np.sin(t)
        x_cord.append(xx)
        y_cord.append(yy)

    points = sort(x_cord,y_cord)

    return points

"""
Main function to run the quickhull algrithm. User can choose to input own
variables, or use the default
"""
def quickhull_run():
    c_gen = False
    y_input = input("Enter 'y' to use own inputs, otherwise enter any character for default parameters: ")
    if y_input == 'y':
        valid = False
        while valid is False:
            try:
                point_size = int(input("Enter the number of points (e.g. 1000): "))
                range_up = float(input("Enter the upper range of points (e.g. 1): "))
                range_low = float(input("Enter the lower range of points (e.g. 0): "))
            except ValueError:
                print("Not valid inputs")
            else:
                if point_size >= 3 and range_up >= 0 and range_low < range_up and range_low >= 0:
                    valid = True
                else:
                    print("Not valid inputs")
    else:
        point_size,range_up,range_low = 2000, 1, 0
        print("Using default")
        y_input = input("Enter 'y' to generate_cirle, otherwise enter any character for default parameters: ")
        if y_input == 'y':
            c_gen = True
            print("Generating circle")

    if c_gen is True:
        points_list = generate_cirle()
    else:
        points_list = generate_points(point_size,range_up,range_low)
    left_mp, right_mp = distance_points(points_list, range_up,range_low)
    above_array, below_array = line_sort(points_list, left_mp, right_mp)
    above_hull = above_sort(above_array, left_mp, right_mp, range_low)
    below_hull = below_sort(below_array, left_mp, right_mp, range_up)
    hull_sort(above_hull, below_hull, points_list)

if __name__ == "__main__":
    start = timeit.default_timer()
    quickhull_run()
    stop = timeit.default_timer()
    print('Time: ', stop - start)
