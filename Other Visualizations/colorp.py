import plotly.express as px
z = [[22.89,2.49,3.81,8.60,35.93,33.62],[5.47,1.81,2.18,2.61,5.57,4.66],[36.81,5.15,3.00,3.95,4.31,5.25],[7.18,3.52,5.85,6.60,5.62,3.25]]
patch=[['A1','A2','A3','A4','A5','A6'],['B1','B2','B3','B4','B5','B6'],['C1','C2','C3','C4','C5','C6'],['D1','D2','D3','D4','D5','D6']]
fig = px.imshow(z, aspect = "auto")
for i,r in enumerate(patch):
    for k,c in enumerate(r):
        fig.add_annotation(x=k,y=i,
                           text=c,
                           showarrow=False, textangle=0,hovertext=c,font=dict(family="Courier New, monospace",size=20,
                          color="silver"))
fig.update_layout(title=("Error in color measurement"))  
fig.update_yaxes(matches=None, showticklabels=True, visible=False)
fig.update_xaxes(matches=None, showticklabels=True, visible=False)
fig.layout.height=500
fig.layout.width=800                
fig.show()


