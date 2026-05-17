# REPARTIR EL TRABAJO
def paralelizar(df_limpio, particiones):
    # SE DIVIDE LA INFORMACION EN VARIAS PARTES
    return df_limpio.repartition(particiones)

    
