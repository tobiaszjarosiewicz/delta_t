#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:31:38 2020

@author: tjarosiewicz
"""

import matplotlib.pyplot as plt
import numpy as np


with open('delta.dat', 'r') as f:
    data = f.readlines()


# Plot dimmensions:
p_width = 16
p_heigth = 8


def parse_data(data):
    plot_i = []
    plot_lag = []
    plot_delta = []
    plot_extrapol = []
    plot_wind = []
    results = {}
    results['enum'] = plot_i
    results['lag'] = plot_lag
    results['delta'] = plot_delta
    results['extrapolated'] = plot_extrapol
    results['wound'] = plot_wind
    # Initial values
    lag = 0
    delta = 0
    for i, line in enumerate(data):
        dvalues = line.split()
        if (len(dvalues) > 2 and
            dvalues[1].strip('-').strip('+').isnumeric() is True):
            lag = dvalues[1].strip('+?').lstrip('?')
            results['enum'].append(i)
            results['lag'].append(lag)
            if len(dvalues) > 4:
                results['extrapolated'].append(1)
            else:
                results['extrapolated'].append(0)
            if dvalues[3] == "+":
                results['wound'].append(-1)
            elif dvalues[3] == "++":
                results['wound'].append(1)
            elif dvalues[3] == "+/-":
                results['wound'].append(-3)

    # Calculate delta from lag:
    for i, elem in enumerate(results['lag']):
        try:
            delta = int(results['lag'][i+1]) - int(results['lag'][i])
        except IndexError:
            delta = 0
        results['delta'].append(delta)

    # Differentiate for measured and extrapolated data:
    plot_lag_true = []
    plot_lag_xtpl = []
    plot_delta_true = []
    plot_delta_xtpl = []
    plot_i_true = []
    plot_i_xtpl = []
    results['true lag'] = plot_lag_true
    results['extrapolated lag'] = plot_lag_xtpl
    results['true delta'] = plot_delta_true
    results['extrapolated delta'] = plot_delta_xtpl
    results['true i'] = plot_i_true
    results['extrapolated i'] = plot_i_xtpl
    for i in range(len(plot_i)):
        if plot_extrapol[i] == 0:
            results['true lag'].append(plot_lag[i])
            results['true delta'].append(plot_delta[i])
            results['true i'].append(plot_i[i])
        elif plot_extrapol[i] == 1:
            results['extrapolated lag'].append(plot_lag[i])
            results['extrapolated delta'].append(plot_delta[i])
            results['extrapolated i'].append(plot_i[i])

    results['enum'] = np.asarray(results['enum'])
    results['enum'] = results['enum'].astype(np.int64)
    results['lag'] = np.asarray(results['lag'])
    results['lag'] = results['lag'].astype(np.int64)
    results['delta'] = np.asarray(results['delta'])
    results['delta'] = results['delta'].astype(np.int64)
    results['zero'] = np.zeros(len(results['delta']), dtype=np.int64)
    results['true lag'] = np.asanyarray(results['true lag'], dtype=np.int64)
    results['extrapolated lag'] = np.asanyarray(results['extrapolated lag'],
                                                dtype=np.int64)
    results['true i'] = np.asanyarray(results['true i'], dtype=np.int64)
    results['extrapolated i'] = np.asanyarray(results['extrapolated i'],
                                              dtype=np.int64)
    results['true delta'] = np.asarray(results['true delta'], dtype=np.int64)
    results['extrapolated delta'] = np.asarray(results['extrapolated delta'],
                                               dtype=np.int64)
    results['wound'] = np.asanyarray(results['wound'], dtype=np.int64)

    return results


def plot_lag(inp_dict):
    plt.rcParams['figure.figsize'] = [p_width, p_heigth]
    plt.plot(inp_dict['enum'], inp_dict['lag'], label='cumulative lag')
    plt.plot(inp_dict['true i'],
             inp_dict['true lag'],
             label='measured', color='royalblue', marker='o', linewidth=0)
    plt.plot(inp_dict['extrapolated i'],
             inp_dict['extrapolated lag'],
             label='extrapolated', color='royalblue', marker='x', linewidth=0)
    plt.plot(inp_dict['enum'], inp_dict['zero'], color='black',
             linestyle='dashed', linewidth=2)
    plt.plot(inp_dict['enum'], inp_dict['wound'], label='winding',
             color='green', marker='.', linewidth=0)
    # Manually added timestamp for reset:
    plt.axvline(x=45.5, linewidth=1, color='b', label='reset to 0')
    plt.axvline(x=93.5, linewidth=1, color='b')
    plt.axvline(x=97.5, linewidth=1, color='b')
    plt.axvline(x=150.5, linewidth=1, color='b')
    plt.ylabel('[s]')
    plt.xlabel('[n]')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_delta(inp_dict):
    plt.rcParams['figure.figsize'] = [p_width, p_heigth]
    plt.plot(inp_dict['enum'], inp_dict['delta'], label='daily delta t')
    plt.plot(inp_dict['enum'], inp_dict['zero'], color='black',
             linestyle='dashed', linewidth=2)
    plt.plot(inp_dict['true i'], inp_dict['true delta'], label='measured',
             color='royalblue', marker='o', linewidth=0)
    plt.plot(inp_dict['extrapolated i'], inp_dict['extrapolated delta'],
             label='extrapolated', color='royalblue', marker='x', linewidth=0)
    plt.plot(inp_dict['enum'], inp_dict['wound'], label='winding',
             color='green', marker='.', linewidth=0)
    # Manually added timestamp for reset:
    plt.axvline(x=45.5, linewidth=1, color='b', label='reset to 0')
    plt.axvline(x=93.5, linewidth=1, color='b')
    plt.axvline(x=97.5, linewidth=1, color='b')
    plt.axvline(x=150.5, linewidth=1, color='b')
    plt.ylabel('[s]')
    plt.xlabel('[n]')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_deriv(inp_dict):
    deriv = np.gradient(inp_dict['lag'])
    plt.rcParams['figure.figsize'] = [p_width, p_heigth]
    plt.plot(inp_dict['enum'], inp_dict['delta'], label='daily delta t',
             marker='o')
    plt.plot(inp_dict['enum'], deriv, label='gradient')
    plt.ylabel('[s]')
    plt.xlabel('[n]')
    plt.legend()
    plt.title("Gradient of cumulative lag matching delta t.")
    plt.grid(True)
    plt.show()
