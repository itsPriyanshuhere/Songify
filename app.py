from flask import Flask,render_template,url_for,request,redirect
import numpy as np
import matplotlib.pyplot as mtp
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

app = Flask(__name__)


@app.route('/',methods = ['POST','GET'])


def index():
    if request.method == "POST":
       Song = request.form.get("Song")
       number = int(request.form.get("numb"))
       return open("templates/success.html").read().format(p1=project(Song,number))
    return render_template("index.html")
    

def project(song,num_songs):
    dataset = pd.read_csv("/Users/nimishdureja/Desktop/FLASKINTRODUCTION/data.csv")
    df = dataset[dataset['year'] >= 2000]

    X = df.iloc[:, [0, 14]].values
    y = df.iloc[:, 16].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)


    wcss_list= []

    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', random_state= 42)
        kmeans.fit(X)
        wcss_list.append(kmeans.inertia_)

    kmeans = KMeans(n_clusters=3, init='k-means++', random_state= 42)
    y_predict= kmeans.fit_predict(X)


    cluster_map = pd.DataFrame()
    cluster_map['data_index'] = df.index.values
    cluster_map['cluster'] = kmeans.labels_

    a = cluster_map[cluster_map.cluster == 0]
    list1 = []
    list2 = []
    for i in a['data_index'].values:
        artists = df.iloc[i]['artists']
        name = df.iloc[i]['name']
        list1.append(df.iloc[i]['artists'])
        list2.append(df.iloc[i]['name'])


    b = cluster_map[cluster_map.cluster == 1]
    list3 = []
    list4 = []
    for i in b['data_index'].values:
        artists = df.iloc[i]['artists']
        name = df.iloc[i]['name']
        list3.append(df.iloc[i]['artists'])
        list4.append(df.iloc[i]['name'])

    c = cluster_map[cluster_map.cluster == 2]
    list5 = []
    list6 = []
    for i in c['data_index'].values:
        artists = df.iloc[i]['artists']
        name = df.iloc[i]['name']
        list5.append(df.iloc[i]['artists'])
        list6.append(df.iloc[i]['name'])
    ans_artist = []
    ans_song = []
    
    if song.lower() in [x.lower() for x in list2]:
        for i in range(num_songs):
            val = random.randint(0, len(list1))
            key = list1[val]
            value = list2[val]
            ans_artist.append(key.replace('[', '').replace(']', '').replace("'", ""))
            ans_song.append(value)
    elif song.lower() in [x.lower() for x in list4]:
        for i in range(num_songs):
            val = random.randint(0, len(list3))
            key = list3[val]
            value = list4[val]
            ans_artist.append(key.replace('[', '').replace(']', '').replace("'", ""))
            ans_song.append(value)
    elif song.lower() in [x.lower() for x in list6]:
        for i in range(num_songs):
            val = random.randint(0, len(list5))
            key = list5[val]
            value = list6[val]
            ans_artist.append(key.replace('[', '').replace(']', '').replace("'", ""))
            ans_song.append(value)
    else:
        return("not found")
    ans = {}
    for i in range(len(ans_artist)):
        ans[ans_artist[i]] = ans_song[i]
        
    return(str(ans))

if __name__=="__main__":
    app.run(debug=True)
