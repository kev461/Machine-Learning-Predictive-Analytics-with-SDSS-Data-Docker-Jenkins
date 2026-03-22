from sklearn.model_selection import train_test_split

def dividirClasificacion(dfSDSS):
    x = dfSDSS[['u', 'g', 'r', 'i', 'z', 'redshift']]
    y = dfSDSS['class']
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.3, random_state=42)
    return xTrain, xTest, yTrain, yTest

def dividirRegresion(dfSDSS):
    x = dfSDSS[['u', 'g', 'r', 'i', 'z']]
    y = dfSDSS['redshift']
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.3, random_state=42)
    return xTrain, xTest, yTrain, yTest

def obtenerDatosClustering(dfSDSS):
    lista=[]
    lista.append(dfSDSS[['u', 'g', 'r', 'i', 'z']])
    lista.append(dfSDSS['class'])
    return lista