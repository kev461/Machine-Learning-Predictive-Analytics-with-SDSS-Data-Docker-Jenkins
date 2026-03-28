from sklearn.neighbors import KNeighborsClassifier

# Aquí el programa aprende a reconocer qué es cada cosa mirando ejemplos y viendo cuáles se parecen entre sí.
def entrenarKNN(xTrain, yTrain, vecinos=5):
    modelo = KNeighborsClassifier(n_neighbors=vecinos)
    modelo.fit(xTrain, yTrain)
    return modelo