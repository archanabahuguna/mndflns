#******************************************************************

#* Archana Bahuguna Plotting a radial chart */

#******************************************************************
from collections import OrderedDict
from math import log, sqrt

import numpy as np
import pandas as pd
from six.moves import cStringIO as StringIO

from bokeh.plotting import *
"""
eventtitle,prefearfactor,postfearfactor
toastmasters1,8,4
toastmasters2,7,2
toastmasters3,6,4
toastmasters4,8,5
toastmasters5,6,1
toastmasters6,7,4
toastmasters7,5,5
toastmasters8,5,2
toastmasters9,8,7
"""
rating_color = OrderedDict([
    ("Predictedfear", "#0d3362"),
    ("Actualfear", "#c64737")
])

"""
feartype_color = {
    "publicspeaking" : "#aeaeb8",
    "socialanxiety"  : "#e69584",
    "financialrisk"  : "#ccffff",
    "performance"    : "#ccffee",
    "relationships"  : "#abcdef"
}"""


"""Arch: Need to change this to reading all data from db"""

df = pd.read_csv("bk1.csv", skiprows=0)

#------------------------------------------------------------------------------------
width = 800
height = 800
inner_radius = 90
outer_radius = 300 - 10

minr = sqrt(log(.001 * 1E4))
maxr = sqrt(log(1000 * 1E4))
a = (outer_radius - inner_radius) / (minr - maxr)
b = inner_radius - a * maxr

def rad(mic):
    return a * np.sqrt(np.log(mic * 1E4)) + b

big_angle = 2.0 * np.pi / (len(df)) #when len(df) is even: "len(df) +1"
small_angle = big_angle / 2

x = np.zeros(len(df))
y = np.zeros(len(df))

#------------------------------------------------------------------------------------

output_file("radialchart.html", title="radial.py example")

p = figure(plot_width=width, plot_height=height, title="",
    x_axis_type=None, y_axis_type=None,
    x_range=[-420, 420], y_range=[-420, 420],
    min_border=0, outline_line_color=None,
    background_fill="#f0e1d2", border_fill="#f0e1d2")

p.line(x+1, y+1, alpha=0)

# small wedges
angles = np.pi/2 - big_angle/2 - df.index*big_angle
p.annular_wedge(x, y, inner_radius, rad(df.prefearfactor),
    -big_angle+angles, -big_angle+angles+small_angle,
    color=rating_color['Predictedfear'])
p.annular_wedge(x, y, inner_radius, rad(df.postfearfactor),
    -big_angle+angles+small_angle, -big_angle+angles+2*small_angle,
    color=rating_color['Actualfear'])

# radial axes
p.annular_wedge(x, y, inner_radius-10, outer_radius+10,
    -big_angle+angles, -big_angle+angles, color="black")


# bacteria labels
radii=[250]
xr = radii[0]*np.cos(np.array(-big_angle/2 + angles))
yr = radii[0]*np.sin(np.array(-big_angle/2 + angles))
label_angle=np.array(-big_angle/2+angles)
label_angle[label_angle < -np.pi/2] += np.pi # easier to read labels on the left side
p.text(xr, yr, df.eventtitle, angle=label_angle,
    text_font_size="9pt", text_align="center", text_baseline="middle")


# OK, these hand drawn legends are pretty clunky, will be improved in future release
p.rect([-40, -40], [18, 0], width=30, height=13,
    color=list(rating_color.values()))
p.text([-15, -15], [18, 0], text=list(rating_color.keys()),
    text_font_size="9pt", text_align="left", text_baseline="middle")

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

show(p)
