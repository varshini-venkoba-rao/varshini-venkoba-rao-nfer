import plotly.graph_objects as go
df='/home/nference/Videos/varshini/Slides_CS001_Station1_2022-04-25_2022-05-01.csv'
x0 = df['Focus Error Percentage']
x1 = df['Stitching Error Percentage']
fig = go.Figure()
fig.add_trace(go.Histogram(
    x=x0,
    histnorm='percent',
    name='Focus', # name used in legend and hover labels
    xbins=dict( # bins used for histogram
        start=0,
        end=30.0,
        size=1
    ),
    marker_color='#EB89B5',
    opacity=0.75
))
fig.add_trace(go.Histogram(
    x=x1,
    histnorm='percent',
    name='Stitching',
    xbins=dict(
        start=0,
        end=30,
        size=1
    ),
    marker_color='#330C73',
    opacity=0.75
))
fig.update_layout(
    title_text='Distribution of Errors', # title of plot
    xaxis_title_text='Error Value', # xaxis label
    yaxis_title_text='Count', # yaxis label
    bargap=0.2, # gap between bars of adjacent location coordinates
    bargroupgap=0.1 # gap between bars of the same location coordinates
)
fig.show()