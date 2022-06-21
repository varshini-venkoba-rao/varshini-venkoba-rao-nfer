from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
df = pd.read_csv('/home/nference/Videos/varshini/Slides_CS001_Station1_2022-04-25_2022-05-01.csv')
#Stitching Error
lst1 = df['Slide Planarity'].to_list()
lst2=df['Slide Name'].to_list()
newlst1 = np.zeros((30,4), dtype=float)
newlst1[:,0]=lst1[:30]
newlst1[:,1]=lst1[30:60]
newlst1[:,2]=lst1[60:90]
newlst1[:,3]=lst1[90:120]
newlst1 = np.reshape(lst1, (30, 4))
newlst2 = np.zeros((30,4), dtype= object)
newlst2[:,0]=lst2[:30]
newlst2[:,1]=lst2[30:60]
newlst2[:,2]=lst2[60:90]
newlst2[:,3]=lst2[90:120]
newlst2 = np.reshape(lst2, (30, 4))
fig = px.imshow(newlst1,aspect = "auto",height=100, title = 'Slide Planarity')
for i,r in enumerate(newlst2):
    for k,c in enumerate(r):
        fig.add_annotation(x=k,y=i,
                           text=c,
                           showarrow=False, textangle=0,hovertext=c,font=dict(family="Courier New, monospace",size=14,color="silver"),
                         )
fig.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = -1,
        dtick = 1
    )
)
fig.update_layout(
    yaxis = dict(
        tickmode = 'linear',
        tick0 = -1,
        dtick = 1
    )
)
fig.layout.height=1500
fig.layout.width=950
fig.show()
# # Focus Error
# lst3 = df['Focus Error Percentage'].to_list()
# lst4=df['Slide Name'].to_list()
# newlst3 = np.zeros((30,4), dtype=float)
# newlst3[:,0]=lst3[:30]
# newlst3[:,1]=lst3[30:60]
# newlst3[:,2]=lst3[60:90]
# newlst3[:,3]=lst3[90:120]
# newlst3 = np.reshape(lst3, (30, 4))
# newlst4 = np.zeros((30,4), dtype= object)
# newlst4[:,0]=lst4[:30]
# newlst4[:,1]=lst4[30:60]
# newlst4[:,2]=lst4[60:90]
# newlst4[:,3]=lst4[90:120]
# newlst4 = np.reshape(lst4, (30, 4))
# fig1 = px.imshow(newlst3,aspect = "auto",height=100, title = 'Basket Focus Error')
# for p,q in enumerate(newlst4):
#     for r,s in enumerate(q):
#         fig1.add_annotation(x=r,y=p,
#                            text=s,
#                            showarrow=False, textangle=0,hovertext=c,font=dict(family="Courier New, monospace",size=14,color="silver"),
#                          )
# fig1.update_layout(
#     xaxis = dict(
#         tickmode = 'linear',
#         tick0 = -1,
#         dtick = 1
#     )
# )
# fig1.update_layout(
#     yaxis = dict(
#         tickmode = 'linear',
#         tick0 = -1,
#         dtick = 1
#     )
# )
# fig1.layout.height=1500
# fig1.layout.width=950
# fig1.show()
# fig = px.imshow(newlst1,aspect = "auto",height=100, title = 'Basket Stitching Error')
# x0 = df['Focus Error Percentage'].to_list()
# x1 = df['Stitching Error Percentage'].to_list()
# fig = go.Figure()
# fig.add_trace(go.Histogram(
#     x=x0,
#     histnorm='percent',
#     name='Focus', # name used in legend and hover labels
#     xbins=dict( # bins used for histogram
#         start=0,
#         end=30.0,
#         size=1
#     ),
#     marker_color='#EB89B5',
#     opacity=0.75
# ))
# fig.add_trace(go.Histogram(
#     x=x1,
#     histnorm='percent',
#     name='Stitching',
#     xbins=dict(
#         start=0,
#         end=30,
#         size=1
#     ),
#     marker_color='#330C73',
#     opacity=0.75
# ))
# fig.update_layout(
#     title_text='Distribution of Errors', # title of plot
#     xaxis_title_text='Error Value', # xaxis label
#     yaxis_title_text='Count', # yaxis label
#     bargap=0.2, # gap between bars of adjacent location coordinates
#     bargroupgap=0.1 # gap between bars of the same location coordinates
# )
# fig.show()