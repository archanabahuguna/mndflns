#******************************************************************

#* Archana Bahuguna Plotting a radial chart */

#******************************************************************
from collections import OrderedDict
from math import log, sqrt

import numpy as np
import pandas as pd
from six.moves import cStringIO as StringIO

from bokeh.plotting import *

"""antibiotics = 
Event title,                     prefearfactor,     postfearfactor,      fear type
Toastmasters speech,             8,                       5,           public speaking
Presentation,                    10,                      3,           public speaking
Meeting with boss,               4,                       2,           performance
Meeting with enemy,              8,                       4,           relationships
"""
"""
rating_color = OrderedDict([
    ("Predicted fear", "#0d3362"),
    ("Actual fear", "#c64737")
])

feartype_color = {
    "publicspeaking" : "#aeaeb8",
    "socialanxiety"  : "#e69584",
    "financialrisk"  : "#ccffff",
    "performance"    : "#ccffee",
    "relationships"  : "#abcdef"
}"""

drug_color = OrderedDict([
    ("Penicillin",   "#0d3362"),
    ("Streptomycin", "#c64737"),
    ("Neomycin",     "black"  ),
])

gram_color = {
    "positive" : "#aeaeb8",
    "negative" : "#e69584",
}

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

big_angle = 2.0 * np.pi / (len(df) + 1)
small_angle = big_angle / 7

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

# annular wedges
import pdb; pdb.set_trace()
#angles = np.pi/2 - big_angle/2 - df.index.to_series()*big_angle
angles = np.pi/2 - big_angle/2 - df.index*big_angle
colors = [gram_color[gram] for gram in df.gram]
p.annular_wedge(
    x, y, inner_radius, outer_radius, -big_angle+angles, angles, color=colors,
)

# small wedges
p.annular_wedge(x, y, inner_radius, rad(df.penicillin),
    -big_angle+angles+5*small_angle, -big_angle+angles+6*small_angle,
    color=drug_color['Penicillin'])
p.annular_wedge(x, y, inner_radius, rad(df.streptomycin),
    -big_angle+angles+3*small_angle, -big_angle+angles+4*small_angle,
    color=drug_color['Streptomycin'])
p.annular_wedge(x, y, inner_radius, rad(df.neomycin),
    -big_angle+angles+1*small_angle, -big_angle+angles+2*small_angle,
    color=drug_color['Neomycin'])

# radial axes
p.annular_wedge(x, y, inner_radius-10, outer_radius+10,
    -big_angle+angles, -big_angle+angles, color="black")


# bacteria labels
import pdb; pdb.set_trace()
radii=[300]
xr = radii[0]*np.cos(np.array(-big_angle/2 + angles))
yr = radii[0]*np.sin(np.array(-big_angle/2 + angles))
label_angle=np.array(-big_angle/2+angles)
label_angle[label_angle < -np.pi/2] += np.pi # easier to read labels on the left side
p.text(xr, yr, df.bacteria, angle=label_angle,
    text_font_size="9pt", text_align="center", text_baseline="middle")


# OK, these hand drawn legends are pretty clunky, will be improved in future release
p.circle([-40, -40], [-370, -390], color=list(gram_color.values()), radius=5)
p.text([-30, -30], [-370, -390], text=["Gram-" + gr for gr in gram_color.keys()],
    text_font_size="7pt", text_align="left", text_baseline="middle")

p.rect([-40, -40, -40], [18, 0, -18], width=30, height=13,
    color=list(drug_color.values()))
p.text([-15, -15, -15], [18, 0, -18], text=list(drug_color.keys()),
    text_font_size="9pt", text_align="left", text_baseline="middle")

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

show(p)
