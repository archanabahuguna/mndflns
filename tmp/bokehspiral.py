from bokeh.embed import autoload_static
from bokeh.resources import CDN
from random import randint

filepath='static/bokeh/plotsp.js'

def plotsprl(events):

    import numpy as np
    from bokeh.plotting import figure, output_file, show
    from bokeh.models import Range1d
    
    # Skip the first point because it can be troublesome
    theta = np.linspace(0, 80*np.pi, 100000)[1:]
    theta2= np.linspace(0, 90*np.pi, 100000)[1:]

    # Compute the radial coordinates for some different spirals
    arch = theta                  # Archimedean
    arch2=theta2

    # Now compute the X and Y coordinates (polar mappers planned for Bokeh later)
    arch_x = arch*np.cos(theta)
    arch_y  = arch*np.sin(theta)
    arch2_x = arch2*np.cos(theta)
    arch2_y  = arch2*np.sin(theta)

    spiral=figure(plot_width=400, plot_height=400, title="GoldenRatio", x_range=Range1d(start=-50, end=50), y_range=Range1d(start=-50, end=50))
    spiral.xgrid.grid_line_color = None
    spiral.ygrid.grid_line_color = None

    spiral.line(arch_x, arch_y, color="#c1ff55", line_width=4)
    spiral.line(arch2_x, arch2_y, color="#b7feea", line_width=10)


    output_file("lines.html")
    show(spiral)      # show the plot
    
    js, tag = autoload_static(spiral, CDN, '/'+filepath+'?id='+str(randint(1, 1000000)))
    with open(filepath, 'w') as f:
        f.write(js)

    return js,tag
