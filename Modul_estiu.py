#Diccionari de temperatures màximes i mínimes a les estacions de Balears

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, FuncFormatter

#Definim una funció que ens torni el valor mitjà de l'inici i el final de l'estiu dels darrers 30 anys.

def mitjanaTmaxE(asset):
#Cream un bucle que ens guardi els noms de les columnes que necessitarem

    columnes_inici_estiu = []
    columnes_final_estiu = []
    ci=1993
    i=0

    while i<30:
        columnes_inici_estiu.append(str(ci+i)+'6')
        columnes_final_estiu.append(str(ci+i)+'9')
        i=i+1

    #Temperatura màxima
    Data_M = pd.ExcelFile(asset)
    BNDC = pd.read_excel(Data_M, 'BNDC')
    NOM = BNDC["NOMBRE"].astype(str)

    TMAX = {}

    for i in range(18, 25):
        column_name = f"TMAX{i}"
        TMAX[column_name] = BNDC[column_name] / 10
        TMAX[column_name] = np.reshape(TMAX[column_name], (1, -1))

    NOM1 = np.reshape(NOM, (1, -1))
    Matriu = np.vstack((NOM1, *[TMAX[column_name] for column_name in TMAX]))

    # Crear un DataFrame a partir de la matriz
    df = pd.DataFrame(Matriu[1:], columns=Matriu[0])

    # Seleccionar columnes per agafar només les del mes de juny (inici estiu)
    columnes_seleccionades_ie = df[columnes_inici_estiu]

    # Seleccionar columnes per agafar només les del mes de septembre (final estiu)
    columnes_seleccionades_fe = df[columnes_final_estiu]

    # Calcular la mitjana dels elements (Temperatura màxima mitjana de l'inici de l'estiu)
    mitjana_ie = np.nanmean(columnes_seleccionades_ie)
    # Calcular la mitjana dels elements (Temperatura màxima mitjana del final de l'estiu)
    mitjana_fe = np.nanmean(columnes_seleccionades_fe)


    # Imprimir la media
    #print(mitjana_ie)
    #print(mitjana_fe)

    return mitjana_ie, mitjana_fe

'''
print("Lluc:")
mitjanaTmaxE('B013-Lluc-TMAX.xlsx')
print("Port:")
mitjanaTmaxE('B228-Portopí-TMAX.xlsx')
print("Cabaneta:")
mitjanaTmaxE('B273-La-Cabaneta-TMAX.xlsx')
print("Aeroport:")
print(mitjanaTmaxE('B278-Palma-Aeropuerto-TMAX.xlsx'))
print("Capdepera:")
mitjanaTmaxE('B569X-Faro-Capdepera-TMAX.xlsx')
print("S'albufera:")
mitjanaTmaxE('B605-Muro-S-Albufera-TMAX.xlsx')
print("Menorca")
mitjanaTmaxE('B893-Menorca-Aeropuerto-TMAX.xlsx')
print("Eivissa:")
mitjanaTmaxE('B954-Ibiza-Aeropuerto-TMAX.xlsx')
'''

def inici_estiu(asset, any):
    #Hem de fer dataframes que recoeixin les dades compreses entre abril i juny de cada any

    requisit, requisitf = mitjanaTmaxE(asset)  # Requisito común a verificar
    #Temperatura màxima

    Data_M = pd.ExcelFile(asset)
    BNDC = pd.read_excel(Data_M, 'BNDC')
    NOM = BNDC["NOMBRE"].astype(str)

    TMAX = {}

    for i in range(1, 32):
        column_name = f"TMAX{i}"
        TMAX[column_name] = BNDC[column_name] / 10
        TMAX[column_name] = np.reshape(TMAX[column_name], (1, -1))

    NOM1 = np.reshape(NOM, (1, -1))
    Matriu = np.vstack((NOM1, *[TMAX[column_name] for column_name in TMAX]))

    # Crear un DataFrame a partir de la matriz
    df = pd.DataFrame(Matriu[1:], columns=Matriu[0])

    contador = 0
    elements_cumpleixen_requisit_inici = []

    columnes_seleccionades_ie = df[[str(any)+'4', str(any)+'5', str(any)+'6', str(any)+'7', str(any)+'8']]
    #print(columnes_seleccionades_ie)
    inici_df = pd.DataFrame(columnes_seleccionades_ie)
    #print(inici_df)

    for columna in inici_df.columns:  # Recorre las columnas del DataFrame
        for i, elemento in enumerate(inici_df[columna]):  # Recorre los elementos de cada columna
            if np.isnan(elemento):  # Ignorar valores NaN
                continue

            if elemento >= requisit:
                contador += 1
                elements_cumpleixen_requisit_inici.append(str(columna) + str(1 + i))
            else:
                contador = 0
                elements_cumpleixen_requisit_inici = []

            if contador == 7:
                #print(f"inici estiu any {any}:")
                #print(elements_cumpleixen_requisit_inici[0])

                numero=elements_cumpleixen_requisit_inici[0]

                any = numero[:4]

                if numero[4] == "1":
                    mes = numero[4:6]
                    dia = numero[6:]
                else:
                    mes = numero[4]
                    dia = numero[5:]

                return any, mes, dia
            
    return None


m=inici_estiu('B278-Palma-Aeropuerto-TMAX.xlsx',2023)
#print(m)

def final_estiu(asset, any):
    #Hem de fer dataframes que recoeixin les dades compreses entre abril i juny de cada any

    requisit, requisitf = mitjanaTmaxE(asset)  # Requisito común a verificar
    #Temperatura màxima

    Data_M = pd.ExcelFile(asset)
    BNDC = pd.read_excel(Data_M, 'BNDC')
    NOM = BNDC["NOMBRE"].astype(str)

    TMAX = {}

    for i in range(1, 32):
        column_name = f"TMAX{i}"
        TMAX[column_name] = BNDC[column_name] / 10
        TMAX[column_name] = np.reshape(TMAX[column_name], (1, -1))

    NOM1 = np.reshape(NOM, (1, -1))
    Matriu = np.vstack((NOM1, *[TMAX[column_name] for column_name in TMAX]))

    # Crear un DataFrame a partir de la matriz
    df = pd.DataFrame(Matriu[1:], columns=Matriu[0])
    df_invertido_final = df[::-1]
    contador = 0
    elements_cumpleixen_requisit_final = []

    columnes_seleccionades_fe = df_invertido_final[[str(any)+'10', str(any)+'9', str(any)+'8', str(any)+'7', str(any)+'6']]
    #print(columnes_seleccionades_ie)
    final_df = pd.DataFrame(columnes_seleccionades_fe)
    #print(final_df)

    for columna in final_df.columns:  # Recorre las columnas del DataFrame
        for i, elemento in enumerate(final_df[columna]):  # Recorre los elementos de cada columna
            if np.isnan(elemento):  # Ignorar valores NaN
                continue

            if elemento >= requisitf:
                contador += 1
                elements_cumpleixen_requisit_final.append(str(columna) + str(31-i))
            else:
                contador = 0
                elements_cumpleixen_requisit_final = []

            if contador == 7:
                #print(f"final estiu any {any}:")
                #print(elements_cumpleixen_requisit_final)

                numero=elements_cumpleixen_requisit_final[0]

                any = numero[:4]

                if numero[4] == "1":
                    mes = numero[4:6]
                    dia = numero[6:]
                else:
                    mes = numero[4]
                    dia = numero[5:]

                return any, mes, dia
    
    return None
                
                
f=final_estiu('B278-Palma-Aeropuerto-TMAX.xlsx',2020)
#print(f)

def arrays_graficaE(asset, any):
    print(inici_estiu(asset, any))
    if inici_estiu(asset, any)==None:
        f=final_estiu(asset, any)
        if f==None:
            array_y=datetime.datetime(2020, 7, 31)
            array_x = any
            c='green'
            return c, array_y, array_x
        
        else:
            anyf, mesf, diaf = final_estiu(asset, any)
            array_y=datetime.datetime(2020, month=int(mesf), day=int(diaf))
            array_x = any
            c='red'
            return c, array_y, array_x    

    elif final_estiu(asset, any)==None:
        i=inici_estiu(asset, any)
        if i==None:
            array_y=datetime.datetime(2020, 7, 31)
            array_x = any
            c='green'
            return c, array_y, array_x
        else:
            anyi, mesi, diai = inici_estiu(asset, any)
            array_y=datetime.datetime(2020, month=int(mesi), day=int(diai))
            array_x = any
            c='red'
            return c, array_y, array_x

    else:           
        #Cream l'array de dates (l'any que inclourem serà aleatori perquè després farem un altre llista per etiquetar els anys)
        anyi, mesi, diai = inici_estiu(asset, any)
        print(inici_estiu(asset, any))

        anyf, mesf, diaf = final_estiu(asset, any)
        print(final_estiu(asset, any))

        data_inici = datetime.datetime(2020,month=int(mesi), day=int(diai))
        data_final = datetime.datetime(2020,month=int(mesf), day=int(diaf))

        # Calcula la cantidad de días entre la fecha de inicio y la fecha de fin
        num_dias = (data_final - data_inici).days + 1

        # Genera un array de fechas utilizando un bucle for
        array_y = [data_inici + datetime.timedelta(days=i) for i in range(num_dias)]
        array_x = np.full(len(array_y), any)
        #print(array_y)
        #print(len(array_y))
        return array_y, array_x


def colorsE(asset, any):

    requisit, requisitf = mitjanaTmaxE(asset)

    anyi, mesi, diai = inici_estiu(asset, any)
    anyf, mesf, diaf = final_estiu(asset, any)
    i = int(mesi)
    columnes = []

    while i <= int(mesf):
        columnes.append(str(any)+str(i))
        i = i+1

    #Temperatura màxima
    Data_M = pd.ExcelFile(asset)
    BNDC = pd.read_excel(Data_M, 'BNDC')
    NOM = BNDC["NOMBRE"].astype(str)

    TMAX = {}

    for i in range(1, 32):
        column_name = f"TMAX{i}"
        TMAX[column_name] = BNDC[column_name] / 10
        TMAX[column_name] = np.reshape(TMAX[column_name], (1, -1))

    NOM1 = np.reshape(NOM, (1, -1))
    Matriu = np.vstack((NOM1, *[TMAX[column_name] for column_name in TMAX]))

    # Crear un DataFrame a partir de la matriz
    df = pd.DataFrame(Matriu[1:], columns=Matriu[0])
    #print(df)
    df.loc[30, str(any)+'6'] = 'None'
    df.loc[30, str(any)+'9'] = 'None'

    # Seleccionar columnes per agafar només les del mes de juny (inici estiu)
    columnes_seleccionades = df[columnes].transpose()
    #print(columnes_seleccionades)

    array = columnes_seleccionades.values.flatten()
    #print(array)

    if int(diaf)==31:
        intervalo = array[int(diai)-1:]
        #print(intervalo)
        #print(len(intervalo))
    else:
        intervalo = array[int(diai)-1:int(diaf)-31]
        #print(intervalo)
        #print(len(intervalo))

    color = []
    for value in intervalo:
        if value == 'None':
            None
        else:
            if not np.isnan(value):
                if value < requisitf:
                    color.append('green')
                else:
                    color.append('red')
            else:
                color.append('white')

    #print(color)
    #print(len(color))
    return color

def y_formatter(value, _):
    fecha = datetime.datetime.fromordinal(int(value) + datetime.datetime(2000, 1, 1).toordinal()+1)
    return fecha.strftime("%m-%d")


def grafica_estiu(asset, anyi, anyf):
    requisit, requisitf = mitjanaTmaxE(asset)
    yearsi = []
    yearsf=[]
    start_summer=[]
    end_summer=[]
    for any in range(anyi,anyf):
        
        if inici_estiu(asset, any) is None and final_estiu(asset, any) is None:
            c, y, x=arrays_graficaE(asset,any)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c=c, s=5)
        elif inici_estiu(asset, any) is None: 
            yearsf.append(any)
            c, y, x=arrays_graficaE(asset,any)
            end_summer.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c=c, s=5)

        elif final_estiu(asset, any) is None:
            yearsi.append(any)
            c, y, x=arrays_graficaE(asset,any)
            start_summer.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c=c, s=5)

        else:
            y, x=arrays_graficaE(asset,any)

            anyi, mesi, diai = inici_estiu(asset,any)
            anyf, mesf, diaf = final_estiu(asset,any)
            data_inici = datetime.datetime(2020,month=int(mesi), day=int(diai))
            data_final = datetime.datetime(2020,month=int(mesf), day=int(diaf))
            start_summer.append(data_inici)
            end_summer.append(data_final)
            yearsi.append(any)
            yearsf.append(any)

            if len(y)==len(colorsE(asset,any)):
                c=colorsE(asset,any)
            else:
                c='blue'

            plt.scatter(x, y, c=c, s=5)

    start_summer = mdates.date2num(start_summer)
    end_summer = mdates.date2num(end_summer)

    # Ajustar líneas de tendencia utilizando regresión lineal
    start_trend = np.polyfit(yearsi, start_summer, 1)
    end_trend = np.polyfit(yearsf, end_summer, 1)

    start_slope, start_intercept = start_trend
    end_slope, end_intercept = end_trend

    # Calcular los valores predichos para las líneas de tendencia
    start_trend_line = np.polyval(start_trend, yearsi)
    end_trend_line = np.polyval(end_trend, yearsf)

    # Graficar las líneas de tendencia
    plt.plot(yearsi, start_trend_line, 'black', label='Línea de Tendencia (Inicio)')
    plt.plot(yearsf, end_trend_line, 'black', label='Línea de Tendencia (Fin)')

    print("Ecuación de la línea de tendencia (Inicio): y = {}x + {}".format(start_slope, start_intercept))
    print("Ecuación de la línea de tendencia (Fin): y = {}x + {}".format(end_slope, end_intercept))
    print(f"nombre de dies augment inici: {start_slope*10}")
    print(f"nombre de dies augment final: {end_slope*10}")
    
    plt.gca().yaxis.set_major_formatter(FuncFormatter(y_formatter))

    plt.grid()
    plt.title(asset)

    # Configurar los ticks en el eje X para que aparezcan cada dos años
    plt.gca().xaxis.set_major_locator(MultipleLocator(base=2))

    # Configurar los ticks en el eje Y para que aparezcan cada 4 dias
    plt.gca().yaxis.set_major_locator(MultipleLocator(base=4))

    plt.xticks(rotation=90)

    plt.xlabel('any', fontsize=12)
    plt.ylabel('mes-dia', fontsize=12)

    #plt.show()
    #plt.savefig(asset+'estiu.png')


