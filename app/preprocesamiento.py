from sklearn.model_selection import train_test_split

# Separa una parte de la información para que el programa estudie y otra para ver si aprendió a identificar bien las cosas.
def dividirClasificacion(dfSDSS):
    x = dfSDSS[['u', 'g', 'r', 'i', 'z', 'redshift']]
    y = dfSDSS['class']
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.3, random_state=42)
    return xTrain, xTest, yTrain, yTest

# Prepara los datos necesarios para que el programa aprenda a calcular números exactos.
def dividirRegresion(dfSDSS):
    x = dfSDSS[['u', 'g', 'r', 'i', 'z']]
    y = dfSDSS['redshift']
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.3, random_state=42)
    return xTrain, xTest, yTrain, yTest

# Elige los detalles que el programa usará para intentar armar grupos de cosas por su propia cuenta según patrones encontrados.
def obtenerDatosClustering(dfSDSS):
    lista=[]
    lista.append(dfSDSS[['u', 'g', 'r', 'i', 'z']])
    lista.append(dfSDSS['class'])
    return lista