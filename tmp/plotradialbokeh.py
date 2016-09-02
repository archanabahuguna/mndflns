########################################################################################
#
#   File Name      Date          Owner            Description
#   ----------    -------      ----------       ----------------
#   plotradialbokeh.py   4/4/2015   Archana Bahuguna  Plots radial chart using bokeh lib
#
#######################################################################################

from collections import OrderedDict
from math import log, sqrt

import numpy as np
import pandas as pd

#from bokeh.models import OpenURL, TapTool
from bokeh.embed import autoload_static
from bokeh.resources import CDN

from bokeh.plotting import *
from random import randint
import os
filepath='static/bokeh/radial.js'

def plotradial(events):

    rating_color = OrderedDict([
        ("Actualfear", "#c1ff55"),
        ("Predictedfear", "#b7feea")
        ]) #666699 #b3b3cc


    xr = [x.title for x in events]
    i=[i for i,j in enumerate(events)]
    y1=[y.prefearfactor for y in events]
    y2=[y.postfearfactor for y in events]
    data={'prefearfactor':pd.Series(y1,index=i), 'postfearfactor':pd.Series(y2,index=i)}
    df = pd.DataFrame(data)
    
    """
    For chart with circular circumference--
    y=df.prefearfactor+df.postfearfactor
    df.prefearfactor=(df.prefearfactor*20.0)/y
    df.postfearfactor=(df.postfearfactor*20.0)/y
    """
    #------------------------------------------------------------------------------------
    width = 500 #400
    height = 420 #350
    inner_radius = 60 #50
    outer_radius = 440 - 20 #360 - 10  

    #Since we are plotting stacked bar charts in a radial axes for pre and post factors and
    #both can have values from 0 through 10, the minr =0 (if both are 0) and maxr=20 if both=10
    minr = 0
    maxr = 20
    #Hence the min length that can be plotted along the radial axes
    min_pixel = (outer_radius - inner_radius) / (maxr - minr)

    big_angle = 2.0 * np.pi / (len(df)) #when len(df) is even: "len(df) +1"
    #small_angle = big_angle / 2
    x = np.zeros(len(df))
    y = np.zeros(len(df))
    
    #------------------------------------------------------------------------------------
    output_file("radialchart.html", title="radial.py example")

    p = figure(plot_width=width, plot_height=height, title="Imagined vs real fear",
        x_axis_type=None, y_axis_type=None, toolbar_location=None,
        x_range=[-420, 420], y_range=[-420, 420],
        min_border=0, outline_line_color=None,
        background_fill="#f8f8f8", border_fill="#f8f8f8")

    #p.line(x+1, y+1, alpha=0)

    # small wedges
    angles = np.pi/2 - big_angle/2 - df.index*big_angle

    p.annular_wedge(x, y, inner_radius, inner_radius+min_pixel*(df.postfearfactor),
                    -big_angle+angles, angles,color=rating_color['Actualfear'])
    p.annular_wedge(x, y, inner_radius+min_pixel*(df.postfearfactor), 
                 inner_radius+min_pixel*(df.postfearfactor)+min_pixel*(df.prefearfactor),
                -big_angle+angles, angles, color=rating_color['Predictedfear'])

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

    # [x1,x2], [y1,y2] is for rect1 and rect2 x and y start positions (y is inverted)
    p.rect([180, 180], [380, 340], width=30, height=20,
            color=list(rating_color.values()))
    #similarly for the legend text
    p.text([200, 200], [365, 325], text=list(rating_color.keys()),
            text_font_size="10pt", text_align="left", text_baseline="bottom")

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    #show(p)  - commented out so it doesnt try to open display in linux
    """
    url = "http://192.168.33.10:5005/users/1/pages/1/txteventsresultsummary"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)
    """
    #There are also these cache control examples you want to checkout - 
    #http://stackoverflow.com/questions/11356188/flask-static-file-cache-control    
    js, tag = autoload_static(p, CDN, '/'+filepath+'?id='+str(randint(1, 1000000)))

    with open(filepath, 'w') as f:
        f.write(js)

    return js,tag

