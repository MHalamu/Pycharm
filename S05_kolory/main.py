#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import math
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import sys


def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')


def normalize_v(v, no_of_turns):
    """Normalize v to range 0-1 for each turn in the color scheme."""

    # Length of single path, e.g. when 3 turns are used, the single path length will be 0.333.
    single_path_length = math.floor(1 / float(no_of_turns) * 10000) / 10000.0

    # Points indicates the turn, e.g. when 3 turns are used, turn_points are 0, 0.333, 0.666, 1.
    turn_points = np.linspace(0, 1, no_of_turns + 1)

    for current_turn in range(no_of_turns):
        if turn_points[current_turn] <= v <= turn_points[current_turn + 1]:
            v_norm = (v - turn_points[current_turn]) / single_path_length
            return v_norm, current_turn


def calculate_colors(v_norm, paths, current_turn):
    """Calculate color based on path traced in colors space.
       Path is represented as a list of (x, y, z) points which described specific color."""
    return_colors = [0, 0, 0]
    for color_num in range(3):
        if paths[current_turn][color_num] == paths[current_turn+1][color_num]:
            return_colors[color_num] = paths[current_turn][color_num]

        elif paths[current_turn+1][color_num] > paths[current_turn][color_num]:
            return_colors[color_num] = paths[current_turn][color_num] + (
                    paths[current_turn+1][color_num] - paths[current_turn][color_num])*v_norm

        elif paths[current_turn+1][color_num] < paths[current_turn][color_num]:
            return_colors[color_num] = paths[current_turn][color_num] - (
                    paths[current_turn][color_num] - paths[current_turn+1][color_num]) * v_norm

    return return_colors


def hsv2rgb(h, s, v):
    c = v * float(s)
    x = c * float(1 - abs((h/60.0) % 2 - 1))
    m = v - c
    if 0 <= h < 60:
        r_, g_, b_ = c, x, 0
    elif 60 <= h < 120:
        r_, g_, b_ = x, c, 0
    elif 120 <= h < 180:
        r_, g_, b_ = 0, c, x
    elif 180 <= h < 240:
        r_, g_, b_ = 0, x, c
    elif 240 <= h < 300:
        r_, g_, b_ = x, 0, c
    elif 300 <= h < 360:
        r_, g_, b_ = c, 0, x
    else:
        return 0, 0, 0

    return r_ + m, g_ + m, b_ + m


def gradient_rgb_bw(v):
    return v, v, v


def gradient_rgb_gbr(v):

    # Shortest path: green, blue, red,
    paths = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]

    v_norm, current_turn = normalize_v(v, len(paths) - 1)
    rgb_tuple = calculate_colors(v_norm, paths, current_turn)

    return rgb_tuple


def gradient_rgb_gbr_full(v):

    # Full path from green to red
    paths = [[0, 1, 0], [0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0]]

    v_norm, current_turn = normalize_v(v, len(paths) - 1)
    # -1 because if there are 5 points, there are only 4 sections between points

    rgb_tuple = calculate_colors(v_norm, paths, current_turn)

    return rgb_tuple


def gradient_rgb_wb_custom(v):
    paths = [(1, 1, 1), (0, 1, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0)]

    v_norm, current_turn = normalize_v(v, len(paths) - 1)
    # -1 because if there are 5 points, there are only 4 sections between points
    rgb_tuple = calculate_colors(v_norm, paths, current_turn)

    return rgb_tuple


def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):

    # red -> h=0, s=1, v=1
    # green -> h=120, s=1, v=1
    # blue -> h=240, s=1, v=1

    # Green, blue, red
    paths = [(120, 1, 1), (240, 1, 1), (360, 1, 1)]
    v_norm, current_turn = normalize_v(v, len(paths) - 1)
    hsv_tuple = calculate_colors(v_norm, paths, current_turn)

    return hsv2rgb(*hsv_tuple)


def gradient_hsv_unknown(v):
    paths = [(120, 0.5, 1), (4, 0.5, 1)]

    v_norm, current_turn = normalize_v(v, len(paths) - 1)
    hsv_tuple = calculate_colors(v_norm, paths, current_turn)

    return hsv2rgb(*hsv_tuple)


def gradient_hsv_custom(v):
    paths = [(0, 0.5, 1), (30, 0.75, 1), (60, 1, 1), (90, 0.75, 1), (120, 0.5, 1),
             (150, 0.75, 1), (180, 1, 1), (210, 0.75, 1), (240, 0.5, 1), (270, 0.75, 1),
             (300, 1, 1), (330, 0.75, 1), (360, 0.5, 1)]

    v_norm, current_turn = normalize_v(v, len(paths) - 1)
    hsv_tuple = calculate_colors(v_norm, paths, current_turn)

    return hsv2rgb(*hsv_tuple)


##########################################
# Methods related with map coloring

def get_normalized_height(min_map_point, max_map_point, height):
    return (height - min_map_point) / (max_map_point - min_map_point)


def get_min_max_point(file_path):
    """Get minimal and maximal point of the map."""

    min_map_point = sys.maxsize
    max_map_point = -sys.maxsize

    with open(file_path, 'r') as file:
        width, height, distance = file.readline().strip().split()

        for h in range(int(height)):
            single_map_line = [float(value) for value in file.readline().strip().split()]
            single_line_max = max(single_map_line)
            if single_line_max > max_map_point:
                max_map_point = single_line_max

            single_line_min = min(single_map_line)
            if single_line_min < min_map_point:
                min_map_point = single_line_min

    return min_map_point, max_map_point


def calculate_shadows(single_map_line, rgb_tuple):
    """Calculate shadows by comparing points next to each other.
       If given point is higher than the next on the right, color is
       slightly modified towards red."""
    try:
        if float(single_map_line[i]) < float(single_map_line[i + 1]):
            pass
        elif float(single_map_line[i]) > float(single_map_line[i + 1]):
            rgb_tuple = (float(rgb_tuple[0]) * 1.1, float(rgb_tuple[1]) * 0.9, float(rgb_tuple[2]) * 0.9)
    except IndexError:
        pass

    return rgb_tuple


if __name__ == '__main__':


    ###################################
    # Code related with gradients

    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])

    column_width_pt = 400
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, ax = plt.subplots(sharex=True, figsize=(size, 0.75 * size))


    ###################################
    # Code related with shadows

    min_map_point, max_map_point = get_min_max_point('big.dem')

    # Colors used in map coloring: green->yellow->red
    paths = [[0, 1, 0], [1, 1, 0], [1, 0, 0]]

    with open("big.dem", 'r') as file:
        width, height, distance = file.readline().strip().split()
        img = np.zeros((500, 500, 3))

        for h in range(int(height)):
            # iterate over each horizontal line of map
            single_map_line = [value for value in file.readline().strip().split()]

            for i, map_value in enumerate(single_map_line):
                # Iterate over each value in single map line.

                # normalize height and v.
                norm_height = get_normalized_height(min_map_point, max_map_point, float(map_value))
                v_norm, current_turn = normalize_v(norm_height, len(paths) - 1)

                # calculate color used for coloring given point.
                rgb_tuple = calculate_colors(v_norm, paths, current_turn)

                rgb_tuple_with_shadows = calculate_shadows(single_map_line, rgb_tuple)
                img[h, i] = rgb_tuple_with_shadows

    im = ax.imshow(img, aspect='auto')
    im.set_extent([0, 1, 0, 1])
    ax.yaxis.set_visible(False)

    pos = list(ax.get_position().bounds)
    x_text = pos[0] - 0.25
    y_text = pos[1] + pos[3]/2.
    fig.text(x_text, y_text, 'map', va='center', ha='left', fontsize=10)
    fig.savefig('map.pdf')
