import pandas as pd
import plotly.graph_objects as go
import numpy as np
fileIn = 'region_result_output.xlsx'
xl = pd.ExcelFile(fileIn)
newdf = xl.parse()
newdf.replace(' ', np.nan, inplace=True)
newdf['Ver. PCode'] = newdf['Ver. PCode'].astype(str)
newdf['shipments'] = newdf['House Bill'].astype(str) + '票'
mapboxToken = 'pk.eyJ1IjoiczM3NTA5NTQiLCJhIjoiY2tiZjl3MnZnMGxsdzJxbjRpNDI3a2J3NyJ9.kOhuIXCnopGdLKBVIcvydg'



fig = go.Figure(data=go.Scattermapbox(
    showlegend=False,
    lon=newdf['lng'],
    lat=newdf['lat'],
    mode='markers',
    ids=newdf['cluster'],
    text=newdf[['cluster','id','shipments']].agg(' / '.join, axis=1),
    hoverinfo='all',
    marker=dict(color=newdf['colour'], size=np.log2(newdf['House Bill'])*10, sizemode='area')
))

fig.update_layout(
    title='LP MEL收派分区示意图',
    mapbox=dict(accesstoken=mapboxToken,
                style='light',
                center=dict(lat=newdf['lat'].median(), lon=newdf['lng'].median()),
                zoom=8
                )
)
fig.write_html("visualresult.html")
fig.show()