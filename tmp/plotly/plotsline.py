# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
import views

def eventplot(events):

    import plotly.plotly as py
    #py.sign_in(username='abahuguna', api_key='5gmqkudahe', stream_ids=['avebr1c422', 'mwhbc95775'])
    #plotly should get the above data from ~/.plotly/.credentials file and try to sign in for you
    from plotly.graph_objs import *
    
    trace1 = Scatter(
            x=[i.title for i in events],
            y=[j.prefearfactor for j in events],
            name='Projected fear',
            mode='lines+markers',
            line=Line(color='FF0000', width=4),
            marker=Marker(size=12, symbol="circle-open-dot")
            )

    trace2 = Scatter(
            x=[i.title for i in events],
            y=[j.postfearfactor for j in events],
            name='Actual fear',
            mode='lines+markers',
            line=Line(color='#0000FF', width=4),
            marker=Marker(size=12, symbol="circle-open-dot")
            )

    data = Data([trace1, trace2])
    layout=Layout(
        title='Projected vs Actual',
        titlefont=dict(family='Arial, monospace', size=16, color='#fe2e2e'),
        font=dict(family='Arial, monospace', size=12, color='#ff8000'),
        autosize=False,
        width=600,
        height=400,
        margin=Margin(
            l=50,
            r=50,
            b=50,
            t=50,
            pad=4),
        xaxis=XAxis(title='Events', showgrid=True),
        yaxis=YAxis(title='Factor', showgrid=True)
        #barmode='stack'
           )

    fig=Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='line-scatter', auto_open=False)
    #auto_open blocks plotly from generating the plot locally
    print "************** From plotsline.py- ****************"
    print plot_url

    return plot_url
