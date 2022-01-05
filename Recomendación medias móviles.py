import pandas as pd
import numpy as np

# ----------------------------------
# Importar data
spx_px = pd.read_csv('stocks.csv')
spx_px = spx_px.set_index('Date')
spx_px = spx_px.sort_index()
spx_px = spx_px['S&P 500']
spx_px = spx_px.dropna()
spx_px.index = pd.DatetimeIndex(spx_px.index)

spx_senal = pd.Series(index=spx_px.index) 
spx_ret = spx_px.pct_change()

#Número de periodos medias móviles 
R=10
I=20
L=50

def trend_signal(precios=spx_px,rapida=20,intermedia=50,lenta=200):
    """
    Esta función entrega una recomendación de compra o venta basado la posicion
    de tres medias móviles
    
    Parametros
    ----------
    precios: pandas Series. Contiene la serie de tiempo con los precios a analizar.
    rapida: int. Número de observaciones de la ventana rápida (R).
    intermedia: int. Número de observaciones de la ventana intermedia (I).
    lenta: int. Número de observaciones de la ventana lenta (L).

    Resultado
    ----------
    posicion: int. 1 si el cruce de medias móviles sugiere estar largo, -1 si el cruce de
    medias móviles sugiere estar corto, 0 si el cruce de medias móviles sugiere estar cerrado.

    """

    sma_R = precios[-rapida:].mean()
    sma_I = precios[-intermedia:].mean()
    sma_L = precios[-lenta:].mean()

    posicion = None
    if (sma_R > sma_I) and (sma_R > sma_L):
        print('Tomar posicion larga')
        posicion = 1
        return posicion
    elif (sma_R < sma_I) and (sma_R < sma_L):
        print('Tomar posicion corta')
        posicion = -1
        return posicion
    else:
        print('Cerrar posicion')
        posicion = 0
        return posicion

#Loop que recorre la matriz para calcular la posición en cada una de las fechas

mean_ret = []
fechas = spx_px[L:].index
for t in fechas:
    px = spx_px[:t]
    spx_senal[t] = trend_signal(px,R,I,L)
    if spx_senal[t] == 1:
        mean_ret.append(spx_ret[t] * 1)
    elif spx_senal[t] == -1:
        mean_ret.append(spx_ret[t] * -1)
    elif spx_senal[t] == 0:
        mean_ret.append(spx_ret[t] * 0)


#Correlación

mean_ret=pd.Series(mean_ret)

print(np.correlate(spx_ret,mean_ret))








