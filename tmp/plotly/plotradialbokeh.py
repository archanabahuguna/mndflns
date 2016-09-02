#******************************************************************

#* Archana Bahuguna Plotting a radial chart */

#******************************************************************
from collections import OrderedDict
from math import log, sqrt

import numpy as np
import pandas as pd

from bokeh.models import OpenURL, TapTool
from bokeh.plotting import *
rating_color = OrderedDict([
    ("Predictedfear", "#666699"),
    ("Actualfear", "#b3b3cc")
])


"""Arch: Need to change this to reading all data from db"""
df = pd.read_csv("bk1.csv", skiprows=0)

"""
For chart with circular circumference--
y=df.prefearfactor+df.postfearfactor
df.prefearfactor=(df.prefearfactor*20.0)/y
df.postfearfactor=(df.postfearfactor*20.0)/y
"""
#------------------------------------------------------------------------------------
width = 600
height = 600
inner_radius = 50
outer_radius = 360 - 10

#Since we are plotting stacked bar charts in a radial axes for pre and post factors and
#both can have values from 0 through 10, the minr =0 (if both are 0) and maxr=20 if both=10
minr = 0
maxr = 20
#Hence the min length that can be plotted along the radial axes
min_pixel = (outer_radius - inner_radius) / (maxr - minr)

def rad(val):
    return min_pixel*val

big_angle = 2.0 * np.pi / (len(df)) #when len(df) is even: "len(df) +1"
#small_angle = big_angle / 2
x = np.zeros(len(df))
y = np.zeros(len(df))

#------------------------------------------------------------------------------------
output_file("radialchart.html", title="radial.py example")

p = figure(plot_width=width, plot_height=height, title="Imagined vs real",
    x_axis_type=None, y_axis_type=None,
    x_range=[-420, 420], y_range=[-420, 420],
    min_border=0, outline_line_color=None,
    background_fill="#f8f8f8", border_fill="#f8f8f8")

#p.line(x+1, y+1, alpha=0)

# small wedges
angles = np.pi/2 - big_angle/2 - df.index*big_angle

p.annular_wedge(x, y, inner_radius, inner_radius+rad(df.postfearfactor),
    -big_angle+angles, angles,
    color=rating_color['Actualfear'])
p.annular_wedge(x, y, inner_radius+rad(df.postfearfactor), 
     inner_radius+rad(df.postfearfactor)+rad(df.prefearfactor),
    -big_angle+angles, angles,
    color=rating_color['Predictedfear'])

# radial axes
p.annular_wedge(x, y, inner_radius, outer_radius,
    -big_angle+angles, -big_angle+angles, color="#c2c2d6")
#For shorter radii so the chart looks better-
"""p.annular_wedge(x, y, inner_radius, inner_radius+max(rad(df.prefearfactor))+max(rad(df.postfearfactor)),
    -big_angle+angles, -big_angle+angles, color="#c2c2d6")"""

# bacteria labels
"""
radii=[300]
xr = radii[0]*np.cos(np.array(-big_angle/2 + angles))
yr = radii[0]*np.sin(np.array(-big_angle/2 + angles))
label_angle=np.array(-big_angle/2+angles)
label_angle[label_angle < -np.pi/2] += np.pi # easier to read labels on the left side
p.text(xr, yr, df.eventtitle, angle=label_angle,
    text_font_size="9pt", text_align="center", text_baseline="middle")
"""

# OK, these hand drawn legends are pretty clunky, will be improved in future release
p.rect([160, 160], [360, 340], width=30, height=13,
    color=list(rating_color.values()))
p.text([180, 180], [360, 340], text=list(rating_color.keys()),
    text_font_size="9pt", text_align="left", text_baseline="bottom")

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None


show(p)

url = "http://192.168.33.10:5005/users/1/pages/1/txteventsresultsummary"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

