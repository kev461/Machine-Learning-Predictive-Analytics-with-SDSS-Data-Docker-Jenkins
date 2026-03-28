from sklearn.cluster import KMeans

# Esta parte sirve para que el programa junte las cosas que se parecen y arme grupos por su cuenta.
def entrenarKMeans(datos, numeroClusters=3):
    modelo = KMeans(n_clusters=numeroClusters)
    modelo.fit(datos)
    return modelo