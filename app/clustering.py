from sklearn.cluster import KMeans

def entrenarKMeans(datos, numeroClusters=3):
    modelo = KMeans(n_clusters=numeroClusters)
    modelo.fit(datos)
    return modelo