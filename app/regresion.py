from sklearn.linear_model import LinearRegression

# Aquí el programa aprende a calcular valores numéricos basándose en los patrones que encuentra en la información.
def entrenarRegresion(xTrain, yTrain):
    modelo = LinearRegression()
    modelo.fit(xTrain, yTrain)
    return modelo