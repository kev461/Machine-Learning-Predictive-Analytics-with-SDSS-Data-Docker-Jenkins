from sklearn.linear_model import LinearRegression

def entrenarRegresion(xTrain, yTrain):
    modelo = LinearRegression()
    modelo.fit(xTrain, yTrain)
    return modelo