########################################################################################
#
#   File Name      Date          Owner            Description
#   ----------    -------      ----------       ----------------
#   bokehradial.py   4/4/2015   Archana Bahuguna  Plots radial chart using bokeh lib
#
#######################################################################################

from collections import OrderedDict
from math import log, sqrt

import numpy as np
import pandas as pd

from bokeh.embed import autoload_static
from bokeh.resources import CDN

from bokeh.plotting import *
from random import randint
import os

filepath='static/bokeh/radial'
"""
def gen_radrollingindex():
    for index in xrange(0,65535):
        yield index

rollingindex=gen_radrollingindex()
"""
def plotradial(events, userid):

    rating_color = OrderedDict([
        ("Actualfear", "#c1ff55"),
        ("Predictedfear", "#b7feea")
        ])


    xr = [x.title for x in events]
    i=[i for i,j in enumerate(events)]
    y1=[y.prefearfactor for y in events]
    y2=[y.postfearfactor for y in events]
    data={'prefearfactor':pd.Series(y1,index=i), 'postfearfactor':pd.Series(y2,index=i)}
    df = pd.DataFrame(data)
    
    width = 500 #400
    height = 420 #350
    inner_radius = 60 #50
    outer_radius = 440 - 20 #360 - 10  
    minr = 0
    maxr = 20

    min_pixel = (outer_radius - inner_radius) / (maxr - minr)

    big_angle = 2.0 * np.pi / (len(df)) 

    x = np.zeros(len(df))
    y = np.zeros(len(df))
    
    #------------------------------------------------------------------------------------
    output_file("radialchart.html", title="radial.py example")

    p = figure(plot_width=width, plot_height=height, title="Imagined vs real fear",
        x_axis_type=None, y_axis_type=None, toolbar_location=None,
        x_range=[-420, 420], y_range=[-420, 420],
        min_border=0, outline_line_color=None,
        background_fill="#f8f8f8", border_fill="#f8f8f8")


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


    # [x1,x2], [y1,y2] is for rect1 and rect2 x and y start positions (y is inverted)
    p.rect([180, 180], [380, 340], width=30, height=20,
            color=list(rating_color.values()))
    #similarly for the legend text
    p.text([200, 200], [365, 325], text=list(rating_color.keys()),
            text_font_size="10pt", text_align="left", text_baseline="bottom")
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    #generating unique filenames by- adding userid to a rolledindex
    """
    global rollingindex
    userfilepath = filepath+str(userid)+str(rollingindex.next())+'.js'
    """
    userfilepath=filepath+str(userid)+'.js'
    js, tag = autoload_static(p, CDN, '/'+userfilepath+'?id='+str(randint(1, 1000000)))
    
    with open(userfilepath, 'w') as f:
        f.write(js)

    return js,tag

