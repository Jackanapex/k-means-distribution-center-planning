import convt as cvt
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import datetime as dt

def elbow_chart(df,start,end):
    k_rng = range(start,end)
    sse=[]
    for k in k_rng:
        km = KMeans(n_clusters=k)
        km.fit_predict(df[['current_lat','current_lon']])
        sse.append(km.inertia_)
    print(sse)
    plt.xlabel('K')
    plt.ylabel('Sum of s error')
    plt.plot(k_rng,sse)
    plt.show()



def clustering_chart(df,n_clusters):
    mapboxToken = 'pk.eyJ1IjoiczM3NTA5NTQiLCJhIjoiY2tiZjl3MnZnMGxsdzJxbjRpNDI3a2J3NyJ9.kOhuIXCnopGdLKBVIcvydg'
    km = KMeans(n_clusters=n_clusters)
    y_predicted = km.fit_predict(df[['current_lat', 'current_lon']])
    df['cluster'] = y_predicted
    df['regionName'] = df['cluster']
    df.loc[df['cluster'] == 0, 'regionName'] = 'ALFA'
    df.loc[df['cluster'] == 1, 'regionName'] = 'BRAVO'
    df.loc[df['cluster'] == 2, 'regionName'] = 'CHARLIE'
    df.loc[df['cluster'] == 3, 'regionName'] = 'DELTA'
    df.loc[df['cluster'] == 4, 'regionName'] = 'ECHO'
    dfStat = df['cluster'].value_counts(dropna=False)
    #fig_o = go.Figure(data=[go.Table(header=dict(values=['cluster', 'shipments']),cells=dict(values=[[0,1],[28,14]]))])
    #fig_o.write_html("trainingresult.html")
    #fig_o.show()
    centToJoindf = df.groupby('regionName').agg(work_count=('house_bill','count'),weight_total=('Weight',sum)).reset_index()
    newdf = df.groupby(['current_lat','current_lon','cluster','business_flag']).agg(

        house_bill_count = ('house_bill', 'count'),
        house_bill_first = ('house_bill', 'first'),
        # Get min of the duration column for each group
        total_weight = ('Weight', sum),
        # Get sum of the duration column for each group
        regionName_first = ('regionName','first')
    ).reset_index()

    #newdf.columns = ["_".join(x) for x in newdf.columns.ravel()]
    #print(centToJoindf)
    df.to_csv('cluster_result_Kis%s.csv'%n_clusters,index=False)
    dfInput = df[['house_bill','regionName']].copy()
    dfInput['time_label'] = 'DAY'
    dfInput.to_csv('today_training_result_input_K%s_D%s.csv'%(n_clusters,dt.date.today()+dt.timedelta(days=1)), index=False,sep='|')
    newdf['size']=(newdf['house_bill_count'])
    newdf['colourSet'] = newdf['cluster']
    newdf.loc[newdf['cluster'] == 0, 'colourSet'] = 'red'
    newdf.loc[newdf['cluster'] == 1, 'colourSet'] = 'blue'
    newdf.loc[newdf['cluster'] == 2, 'colourSet'] = 'purple'
    newdf.loc[newdf['cluster'] == 3, 'colourSet'] = 'green'
    newdf.loc[newdf['cluster'] == 4, 'colourSet'] = 'black'
    newdf['total_weight'] = newdf['total_weight'].astype(str)
    centroiddf=DataFrame(km.cluster_centers_,columns=['current_lat','current_lon'])
    centroiddf.to_csv('centroid_result_Kis%s.csv'%n_clusters,index=True)
    #print(centroiddf)
    resultdf = pd.concat([centroiddf,centToJoindf],axis=1,join='inner')
    resultdf.round(0)
    #print(resultdf)
    resultdf['weight_total'] = resultdf['weight_total'].apply(int)
    resultdf['weight_total'] = resultdf['weight_total'].apply(str)
    resultdf['work_count'] = resultdf['work_count'].astype(str)

    fig = go.Figure(data=go.Scattermapbox(
        name='Shipment',
        showlegend=False,
        lon=newdf['current_lon'],
        lat=newdf['current_lat'],
        mode='markers',
        ids=newdf['regionName_first'],
        text=newdf['regionName_first'] + ': ' + newdf['total_weight']+'KG -' +newdf['house_bill_first'],
        hoverinfo='all',
        marker = dict(color=newdf['colourSet'],size=newdf['size'],sizemode='area')
    ))
    fig.add_trace(go.Scattermapbox(
        name='predicted centroids',
        showlegend=False,
        lon=resultdf['current_lon'],
        lat=resultdf['current_lat'],
        marker=dict(symbol='car',size=20),
        text=resultdf['regionName'] + ': ' + resultdf['work_count'] +' jobs ' + resultdf['weight_total'] +'KG',
        hoverinfo='all'
    ))
    fig.update_layout(
        title='LETSPORTAL MEL Delivery Scattering (K=%s) ON %s'
              %(n_clusters,dt.date.today()+dt.timedelta(days=1)),
        width = 1000,
        height = 1500,
        mapbox=dict(accesstoken=mapboxToken,
                    style='streets',
                    center=dict(lat=newdf['current_lat'].median(),lon=newdf['current_lon'].median()),
                    zoom = 10
                    )
    )
    fig.write_html("trainingresult.html")
    fig.show()

pd.set_option('display.max_columns', None)
mel=cvt.datasetClass()
# ROOT_DIR = os.path.dirname(os.path.abspath("top_level_file.txt"))
# DATA_DIR = ROOT_DIR + '\\Data'
# filename = DATA_DIR + '\\melbourne.xlsx'
filename = 'manifest_input.xlsx'

df=mel.xl_convt_df(filename)
elbow_chart(df,1,12)
print('How many cluster do you need to use based on the result of elbow chart?')
n_clusters = int(input())
clustering_chart(df,n_clusters)