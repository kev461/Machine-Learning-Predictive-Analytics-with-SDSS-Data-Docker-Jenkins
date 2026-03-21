from sklearn.neighbors import KNeighborsClassifier

def entrenarKNN(xTrain, yTrain, vecinos=5):
    modelo = KNeighborsClassifier(n_neighbors=vecinos)
    modelo.fit(xTrain, yTrain)
    return modelo