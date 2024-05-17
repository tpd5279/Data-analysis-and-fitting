# -*- coding: utf-8 -*-
"""
Created on Thu May 16 17:05:14 2024

@author: tinad
"""

# Fit a circle to a partial data set using least-squares optimization
# Plot the data set and the fitted circle on a single plot.
# Measure the angle by which the radius needs to a desired cartesian coordinate,and plot perpendicular to the tangent at the
# desired cartesian coordinate

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import least_squares
import os
import csv

# Read the data set
folder_path = 'folder location'
file_name = 'filename.csv'
input1 = os.path.join(folder_path, file_name)
df = pd.read_csv(input1)
df['x'] = x
df['y'] = y

# Function to calculate the distances from the circle's center
def calc_R(c, x, y):
    Ri = np.sqrt((x - c[0])**2 + (y - c[1])**2)
    return Ri

# Function to compute the algebraic distance between the data points and the mean circle
def f_2(c, x, y):
    Ri = calc_R(c, x, y)
    return Ri - Ri.mean()

# Initial guess for the circle's center (x, y) and radius
x_m = np.mean(x)
y_m = np.mean(y)
center_estimate = x_m, y_m

# Use least squares optimization to fit the circle
result = least_squares(f_2, center_estimate, args=(x, y))
center_optimized = result.x

# Calculate the radius from the optimized center
radius_optimized = calc_R(center_optimized, x, y).mean()

# Print the results
print(f"Optimized Center: {center_optimized}")
print(f"Optimized Radius: {radius_optimized}")

# Define parameters of the fitted circle
circle_radius = radius_optimized
x_coordinate = center_optimized[0]
y_coordinate = center_optimized[1]

# Plot the data points and the fitted circle
fig, ax = plt.subplots()
ax.plot(x, y, 'ro', markersize=3, label='Data points')

# Circle
circle = plt.Circle(center_optimized, radius_optimized, color='b', fill=False, label='Fitted circle')
ax.add_artist(circle)

# Add a radius on the circle plot
angle_degrees = 0
angle_radians = np.deg2rad(angle_degrees)
end_point_x = x_coordinate + (circle_radius+0.03)*np.cos(angle_radians)
end_point_y = y_coordinate + (circle_radius+0.03)*np.sin(angle_radians)
plt.plot([x_coordinate, end_point_x], [y_coordinate, end_point_y], color='blue', linestyle='--')

# Specify the desired cartesian coordinate
desired_x = 0
desired_y = 0

# Calculate the angle between the radius and the line connecting the circle center to the desired point
dx = desired_x - x_coordinate
dy = desired_y - y_coordinate
angle2_radians = np.arctan2(dy,dx)
angle2_degrees = np.rad2deg(angle2_radians)
angle2_degrees %=360

# Plot the radius passing through the desired point
end_point2_x = x_coordinate + (circle_radius+0.03)*np.cos(angle2_radians)
end_point2_y = y_coordinate + (circle_radius+0.03)*np.sin(angle2_radians)
plt.plot([x_coordinate, end_point2_x], [y_coordinate, end_point2_y], color='blue', linestyle='-')

# Calculate the slope of the radius
slope_radius = np.tan(angle2_radians)

# Calculate the equation of the tangent line
tangent_slope = -1/slope_radius
tangent_intercept = end_point2_y - tangent_slope*end_point2_x

# Plot the tangent line
x_values = np.linspace(x_coordinate - 2*circle_radius, x_coordinate + 2*circle_radius, 100 )
y_values= tangent_slope*x_values + tangent_intercept
plt.plot(x_values, y_values, colors='green', linestyle='--')

# Formatting plot
ax.set_aspect('equal', adjustable='datalim')
plt.plot()
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Circle Fit to Partial Data Set')
plt.grid(True)
plt.show()

print("Angle of rotation: ", angle2_degrees)
