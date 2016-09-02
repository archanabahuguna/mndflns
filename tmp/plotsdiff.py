# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
import views

def eventplot(events):

    import plotly.plotly as py
    #py.sign_in(username='abahuguna', api_key='5gmqkudahe', stream_ids=['avebr1c422', 'mwhbc95775'])
    #plotly should get the above data from ~/.plotly/.credentials file and try to sign in for you
    from plotly.graph_objs import *
    
    trace1 = Scatter(
            #x=[n for (n,m) in enumerate(events)],
            x=[i.title for i in events],
            y=[(j.prefearfactor+(j.postfearfactor- j.prefearfactor)/2) for j in events],
            error_y=dict(type='data',
                         array=[abs((j.prefearfactor-j.postfearfactor)/2) for j in events],
                         visible=True,
                         color='#64FE2E'),
            name='Projected vs actual',
            mode='markers',
            marker=dict(color='#64FE2E', size=2)
            )

    
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
        yaxis=YAxis(title='Factor', showgrid=True, range=[0,12], autorange=False)
            )
    
    data = Data([trace1])
    
    fig=Figure(data=data, layout=layout)

    plot_url = py.plot(fig, filename='line-scatter', auto_open=False)

    #auto_open blocks plotly from generating the plot locally
    print "************** From plotsline.py- ****************"
    print plot_url

    return plot_url

