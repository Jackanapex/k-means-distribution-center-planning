import convt as cvt,os,numpy as np
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans

def elbow_chart(df,start,end):
    k_rng = range(start,end)
    sse=[]
    for k in k_rng:
        km = KMeans(n_clusters=k)
        km.fit_predict(df[['lat','lng']])
        sse.append(km.inertia_)
    print(sse)
    plt.xlabel('K')
    plt.ylabel('Sum of s error')
    plt.plot(k_rng,sse)
    plt.show()
    
def clustering_chart(df,n_clusters):
    tmp_df_list=[]
    km = KMeans(n_clusters=n_clusters)
    y_predicted = km.fit_predict(df[['lat', 'lng']])
    df['cluster'] = y_predicted
    colors=['black', 'blue', 'purple', 'yellow', 'red', 'lime', 'cyan', 'orange', 'gray']
    for i in range(0,n_clusters,1):
        tmp_df_list.append(df[df.cluster == i])

    for i in range(len(tmp_df_list)):
        plt.scatter(tmp_df_list[i]['lat'], tmp_df_list[i]['lng'], s=15, color=colors[i], alpha=1,edgecolors='k')
    plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], color='purple', marker='*', label='centroid')
    plt.xlabel('lat')
    plt.ylabel("lnt")
    plt.show()



mel=cvt.datasetClass()
ROOT_DIR = os.path.dirname(os.path.abspath("top_level_file.txt"))
DATA_DIR = ROOT_DIR + '\\Data'
filename = DATA_DIR + '\\melbourne.xlsx'

df=mel.xl_convt_df(filename)
elbow_chart(df,1,10)
print('How many cluster do you need to use based on the result of elbow chart?')
n_clusters = int(input())
clustering_chart(df,n_clusters)