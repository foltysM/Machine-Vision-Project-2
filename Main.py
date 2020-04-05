import numpy as np
import math
import matplotlib.pyplot as plt


def distance(a, b):
    # returns distance between two points
    # a[0] is x coordinate, a[1] is y coordinate
    if a[0] < 0:
        if b[0] < 0:
            a_distance = abs(a[0] - b[0])
        else:
            a_distance = abs(a[0]) + b[0]
    else:
        if b[0] < 0:
            a_distance = abs(b[0]) + a[0]
        else:
            a_distance = abs(a[0] - b[0])
    b_distance = abs(a[1] - b[1])

    return math.sqrt(b_distance * b_distance + a_distance * a_distance)


def line_to_point_distance(point, start, end):
    # returns distance between a line and a point
    if start.all() == end.all():
        return distance(point, end)
    else:
        numerator = abs(
            (end[0] - start[0]) * (start[1] - point[1]) -
            (start[0] - point[0]) * (end[1] - start[1])
        )
        denominator = math.sqrt(
            (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
        )
        return numerator / denominator


def iterative(tabb, epsilon):
    # recursive function, returns array of lines created from points
    d_max = 0.0
    index = 0
    for i in range(1, len(tabb) - 1):
        distance = line_to_point_distance(tabb[i], tabb[1], tabb[0])
        if distance > d_max:
            index = i
            d_max = distance

    # if distance is greater than epsilon, call function itself twice, dividing into two subsets
    if d_max > epsilon:
        results = iterative(tabb[:index+1], epsilon)[:-1] + iterative(tabb[index:], epsilon)
    else:
        results = [tabb[0], tabb[-1]]

    return results


file = open('r.txt')  # reads data from file

# transforms into cartesian coordinate system
tabx = []
taby = []
i = 0
irad = 0
for line in file:
    r = float(line)
    tabx.append(r*math.cos(irad))
    taby.append(r*math.sin(irad))
    i = i + 1
    # converts to radians
    irad = (math.pi*i)/180

file.close()

plt.scatter(tabx, taby, 1)
plt.show()

# PART 1: Line detection using Ramer–Douglas–Peucker algorithm

tab = np.zeros((180, 2), float)
for i in range(180):
    tab[i][0] = tabx[i]
    tab[i][1] = taby[i]

results = iterative(tab, 0.01)
plt.plot(results)
plt.show()

# PART 2: Creation of an image with positions of obstacles

# creates an array
image_obstacles = np.zeros((602, 602), int)

for j in range(180):
    x_value = tabx[j]
    # need to convert to int, array values are ints
    x_value_int = int(x_value) + 300
    y_value = taby[j]
    y_value_int = int(y_value) + 300
    # if there was an object, value is 255
    image_obstacles[x_value_int][y_value_int] = 255

plt.imshow(image_obstacles)
plt.show()

# PART 3: Line detection using Hough transform

votes_counter = np.zeros(180, int)

ro = np.zeros((180, 180), float)
############################
for i in range(180):
    # just for 180 degrees, for 360 we double results
    for theta in range(180):
        # converts to radians, need it to use in math.cos & math.sin
        theta_radians = (theta * math.pi) / 180
        ro[i][theta] = (tabx[i] * math.cos(theta_radians) + taby[i] * math.sin(theta_radians))

ro_2 = np.zeros((180, 180), float)
for i in range(180):
    for j in range(180):
        # round to 3 decimal places, in order to avoid errors
        ro_2[i][j] = round(ro[i][j], 3)

first_ro = 0
second_ro = 0
first_theta = 0
second_theta = 0
for t in range(180):
    for i in range(180):
        for j in range(180):
            if i != j and ro_2[i][t] == ro_2[j][t]:
                votes_counter[t] = votes_counter[t] + 1
                if votes_counter[t] == 5:
                    print("There is a line in theta ", t)
