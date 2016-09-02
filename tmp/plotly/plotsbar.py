# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api
import views

def eventplot(events):

    import plotly.plotly as py
    #py.sign_in(username='abahuguna', api_key='5gmqkudahe', stream_ids=['avebr1c422', 'mwhbc95775'])
    #plotly should get the above data from ~/.plotly/.credentials file and try to sign in for you
    from plotly.graph_objs import *

    trace1 = Bar(
            x=[i.title for i in events],
            y=[j.prefearfactor for j in events],
            name='Projected',
            marker=dict(color='#64FE2E')
            )

    trace2 = Bar(
            x=[i.title for i in events],
            y=[j.postfearfactor for j in events],
            name='Actual',
            marker=dict(color='#2EFEC8')
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
        yaxis=YAxis(title='Factor', showgrid=True, range=[0,15], autorange=False, gridwidth=2),
        barmode='group',
        bargap=0.1
           )

    fig=Figure(data=data, layout=layout)

    plot_url = py.plot(fig, filename='size-margins', auto_open=False)
    print "**************"
    print plot_url

    return plot_url
