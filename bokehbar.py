###########################################################################
#
#   File Name      Date          Owner            Description
#   ----------    -------      ----------       ----------------
#   bokehbar.py   4/4/2015   Archana Bahuguna  Creates bar chart using bokeh lib
#
###########################################################################


from collections import OrderedDict
from bokeh.embed import autoload_static
from bokeh.resources import CDN
from random import randint
from bokeh.charts import Bar
from bokeh.plotting import output_file, show

filepath='static/bokeh/bar'
"""
def gen_barrollingindex():
    for index in xrange(0,65535):
        yield index

rollingindex=gen_barrollingindex()
"""
def plotbar(events, userid):

    """
    Arch: I tried to install bokeh 0.10.0 ver and that was
    giving a lot of errors in the Bar(method args)- StopIteration
    and also while trying to load the latest bokeh.min.js from CDN
    So I am going back to the bokeh 0.8.1 ver- at least it works
    """
    
    xr = [x.title for x in events]
    y1values=[y1.prefearfactor for y1 in events]
    y2values=[y2.postfearfactor for y2 in events]
    yr=OrderedDict(PredictedFear=y1values, ActualFear=y2values)

    """
    height=400
    width=600
    bar = figure(plot_width=width, plot_height=height, title="Imagined vs real")
    # use the `rect` renderer to display stacked bars of the medal results. Note
    # that we set y_range explicitly on the first renderer
    bar.rect(xr, y1values, height=0.5, width=0.4, color="red", alpha=0.6)
    bar.rect(xr, y2values, height=0.5, width=0.4, color="blue", alpha=0.6)
    """    

    bar=Bar(yr, xr, xlabel="Events", ylabel="Fear factor", title="Imagined vs real fear", width=800, height=600,
           legend=True, palette=['#c1ff55', '#b7feea'], stacked=True, tools=None, xgrid=None, ygrid=None)
    bar.toolbar_location=None

    #output_file("stacked_bar.html", autosave=True)
    #show(bar) - commented out so it doesnt try to open display in linux

    #generating unique filenames by- concatenating userid to a rolledindex- 
    #we dont expect a user to generate more than 
    """
    global rollingindex
    userfilepath = filepath+str(userid)+str(rollingindex.next())+'.js'
    """
    userfilepath=filepath+str(userid)+'.js'
    js, tag = autoload_static(bar, CDN, '/'+userfilepath+'?id='+str(randint(1, 1000000)))

    with open(userfilepath, 'w') as f:
        f.write(js)

    return js,tag
