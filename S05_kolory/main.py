#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import math
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True)
    #rc('font', family='serif', serif=['Times'], size=10)
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
    """Normalize v to range 0-1 for each turn in the color scheme. """

    # Length of single path, e.g. when 3 turns are used, the single path length will be 0.333.
    single_path_length = math.floor(1 / float(no_of_turns) * 10000) / 10000.0

    # Points indicates the turn, e.g. when 3 turns are used, turn_points are 0, 0.333, 0.666, 1.
    turn_points = np.linspace(0, 1, no_of_turns + 1)

    for current_turn in range(no_of_turns):
        if turn_points[current_turn] <= v <= turn_points[current_turn + 1]:
            v_norm = (v - turn_points[current_turn]) / single_path_length
            return v_norm, current_turn

def calculate_colors(v_norm, paths, current_turn):
    return_colors = [0, 0, 0]
    for color_num in range(3):
        if paths[current_turn][color_num] == paths[current_turn+1][color_num]: # if color == color_next:
            return_colors[color_num] = paths[current_turn][color_num]
        elif paths[current_turn+1][color_num] > paths[current_turn][color_num]:
            return_colors[color_num] = paths[current_turn][color_num] + (paths[current_turn+1][color_num] - paths[current_turn][color_num])*v_norm
        elif paths[current_turn+1][color_num] < paths[current_turn][color_num]:
            return_colors[color_num] = paths[current_turn][color_num] - (paths[current_turn][color_num] - paths[current_turn+1][color_num]) * v_norm
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

    paths = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]  # zielony czerwony najkrotsza sciezka

    v_norm, current_turn = normalize_v(v, len(paths) - 1)
    rgb_tuple = calculate_colors(v_norm, paths, current_turn)

    return rgb_tuple


def gradient_rgb_gbr_full(v):
    paths = [[0, 1, 0], [0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 0, 0]] # przejscie z zielonego na czerwony

    v_norm, current_turn = normalize_v(v, len(paths) - 1)  # -1 because if there are 5 points, there are only 4 sections between points
    rgb_tuple = calculate_colors(v_norm, paths, current_turn)

    return rgb_tuple


def gradient_rgb_wb_custom(v):
    paths = [(1, 1, 1), (0, 1, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0)]

    v_norm, current_turn = normalize_v(v, len(paths) - 1)  # -1 because if there are 5 points, there are only 4 sections between points
    rgb_tuple = calculate_colors(v_norm, paths, current_turn)
    print(rgb_tuple)
    return rgb_tuple


def gradient_hsv_bw(v):
    print(hsv2rgb(0, 0, 1))
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):

    # red -> h=0, s=1, v=1
    # green -> h=120, s=1, v=1
    # blue -> h=240, s=1, v=1

    paths = [(120, 1, 1), (240, 1, 1), (360, 1, 1)]
    #paths = [(360, 1, 1), (240, 1, 1), (120, 1, 1)]
    v_norm, current_turn = normalize_v(v, len(paths) - 1)
    hsv_tuple = calculate_colors(v_norm, paths, current_turn)


    return hsv2rgb(*hsv_tuple)

def gradient_hsv_unknown(v):
    paths = [(120, 0.5, 1), (4, 0.5, 1)]

    v_norm, current_turn = normalize_v(v, len(paths) - 1)
    hsv_tuple = calculate_colors(v_norm, paths, current_turn)


    return hsv2rgb(*hsv_tuple)


def gradient_hsv_custom(v):
    paths = [(0, 0.5, 1), (30, 0.75, 1), (60, 1, 1), (90, 0.75, 1), (120, 0.5, 1), (150, 0.75, 1), (180, 1, 1), (210, 0.75, 1),
             (240, 0.5, 1), (270, 0.75, 1), (300, 1, 1), (330, 0.75, 1), (360, 0.5, 1)]

    v_norm, current_turn = normalize_v(v, len(paths) - 1)
    hsv_tuple = calculate_colors(v_norm, paths, current_turn)


    return hsv2rgb(*hsv_tuple)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
