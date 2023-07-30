#Diccionari de temperatures màximes i mínimes a les estacions de Balears

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, FuncFormatter

#Definim una funció que ens torni el valor mitjà de l'inici i el final de la tardor dels darrers 30 anys.
#Tenim en compte que per necessitat del programa el gener és el mes 0 i no 1.
def mitjanaTmaxT(asset):
#Cream un bucle que ens guardi els noms de les columnes que necessitarem

    columnes_inici_tardor = []
    columnes_final_tardor = []
    ci=1993
    i=0

    while i<30:
        columnes_inici_tardor.append(str(ci+i)+'9')
        columnes_final_tardor.append(str(ci+i)+'12')
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

    # Seleccionar columnes per agafar només les del mes de setembre (inici tardor)
    columnes_seleccionades_it = df[columnes_inici_tardor]

    # Seleccionar columnes per agafar només les del mes de septembre (final tardor)
    columnes_seleccionades_ft = df[columnes_final_tardor]

    # Calcular la mitjana dels elements (Temperatura màxima mitjana de l'inici de la tardor)
    mitjana_it = np.nanmean(columnes_seleccionades_it)
    # Calcular la mitjana dels elements (Temperatura màxima mitjana del final de la tardor)
    mitjana_ft = np.nanmean(columnes_seleccionades_ft)


    # Imprimir la media
    #print(mitjana_it)
    #print(mitjana_ft)

    return mitjana_it, mitjana_ft

'''
print("Lluc:")
mitjanaTmaxT('B013-Lluc-TMAX.xlsx')
print("Port:")
mitjanaTmaxT('B228-Portopí-TMAX.xlsx')
print("Cabaneta:")
mitjanaTmaxT('B273-La-Cabaneta-TMAX.xlsx')
print("Aeroport:")
print(mitjanaTmaxT('B278-Palma-Aeropuerto-TMAX.xlsx'))
print("Capdepera:")
mitjanaTmaxT('B569X-Faro-Capdepera-TMAX.xlsx')
print("S'albufera:")
mitjanaTmaxT('B605-Muro-S-Albufera-TMAX.xlsx')
print("Menorca")
mitjanaTmaxT('B893-Menorca-Aeropuerto-TMAX.xlsx')
print("Eivissa:")
mitjanaTmaxT('B954-Ibiza-Aeropuerto-TMAX.xlsx')
'''
#Feim que l'inici de la tardor coincideixi amb el final de l'estiu

def inici_tardor(asset, any):

    requisit, requisitf = mitjanaTmaxT(asset)  # Requisito común a verificar
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

            if elemento >= requisit:
                contador += 1
                elements_cumpleixen_requisit_final.append(str(columna) + str(31-i))
            else:
                contador = 0
                elements_cumpleixen_requisit_final = []

            if contador == 7:
                #print(f"final tardor any {any}:")
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


m=inici_tardor('B278-Palma-Aeropuerto-TMAX.xlsx',2020)
#print(m)

def final_tardor(asset, any):
    #Hem de fer dataframes que recoeixin les dades compreses entre octubre i gener de cada any

    requisit, requisitf = mitjanaTmaxT(asset)  # Requisito común a verificar
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

    columnes_seleccionades_fe = df_invertido_final[[str(any+1)+'0', str(any)+'12', str(any)+'11', str(any)+'10', str(any)+'9']]
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
                #print(f"final tardor any {any}:")
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
                
                
f=final_tardor('B278-Palma-Aeropuerto-TMAX.xlsx',2020)
#print(f)

def arrays_graficaT(asset, any):
    print(inici_tardor(asset, any))
    print(final_tardor(asset, any))
    if inici_tardor(asset, any)==None:
        f=final_tardor(asset, any)
        if f==None:
            array_y=datetime.datetime(2019, 10, 31)
            array_x = any
            c='green'
            return c, array_y, array_x
        
        else:
            anyf, mesf, diaf = final_tardor(asset, any)
            if int(mesf) == 0:
                array_y=datetime.datetime(2020, month=1, day=int(diaf))
            else:
                array_y=datetime.datetime(2019, month=int(mesf), day=int(diaf))
            array_x = any
            c='red'
            return c, array_y, array_x    

    elif final_tardor(asset, any)==None:
        i=inici_tardor(asset, any)
        if i==None:
            array_y=datetime.datetime(2019, 10, 31)
            array_x = any
            c='green'
            return c, array_y, array_x
        else:
            anyi, mesi, diai = inici_tardor(asset, any)
            if int(mesi)==0:
                array_y=datetime.datetime(2020, month=1, day=int(diai))
            else:
                array_y=datetime.datetime(2019, month=int(mesi), day=int(diai))
            array_x = any
            c='red'
            return c, array_y, array_x

    else:           
        #Cream l'array de dates (l'any que inclourem serà aleatori perquè després farem un altre llista per etiquetar els anys)
        anyi, mesi, diai = inici_tardor(asset, any)
        #print(inici_tardor(asset, any))

        anyf, mesf, diaf = final_tardor(asset, any)
        #print(final_tardor(asset, any))

        if int(mesi)==0:
            data_inici = datetime.datetime(2020,month=1, day=int(diai))
            data_final = datetime.datetime(2019,month=int(mesf), day=int(diaf))
        elif int(mesf)==0:
            data_inici = datetime.datetime(2019,month=int(mesi), day=int(diai))
            data_final = datetime.datetime(2020,month=1, day=int(diaf))
        else:
            data_inici = datetime.datetime(2019,month=int(mesi), day=int(diai))
            data_final = datetime.datetime(2019,month=int(mesf), day=int(diaf))                        

        # Calcula la cantidad de días entre la fecha de inicio y la fecha de fin
        num_dias = (data_final - data_inici).days + 1

        # Genera un array de fechas utilizando un bucle for
        array_y = [data_inici + datetime.timedelta(days=i) for i in range(num_dias)]
        array_x = np.full(len(array_y), any)
        #print(array_y)
        #print(len(array_y))
        return array_y, array_x


def colorsT(asset, any):

    requisit, requisitf = mitjanaTmaxT(asset)

    anyi, mesi, diai = inici_tardor(asset, any)
    anyf, mesf, diaf = final_tardor(asset, any)

    if int(mesf)==0:
        i = int(mesi)
        j = 13
    else:
        i = int(mesi)
        j = int(mesf)

    columnes = []

    while i <= j:
        if i==13:
            columnes.append(str(any+1)+"0")
            i = i+1
        else:
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
    df.loc[30, str(any)+'11'] = 'None'

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


def grafica_tardor(asset, anyi, anyf):
    requisit, requisitf = mitjanaTmaxT(asset)
    yearsi = []
    yearsf = []
    start_fall=[]
    end_fall=[]
    for any in range(anyi,anyf):
        
        if inici_tardor(asset, any) is None:
            c, y, x=arrays_graficaT(asset,any)
            end_fall.append(y)
            yearsf.append(any)
            plt.scatter(x, y, c=c, s=5)

        elif final_tardor(asset, any) is None:
            c, y, x=arrays_graficaT(asset,any)
            start_fall.append(y)
            yearsi.append(any)
            plt.scatter(x, y, c=c, s=5)

        else:
            y, x=arrays_graficaT(asset,any)

            anyi, mesi, diai = inici_tardor(asset,any)
            anyf, mesf, diaf = final_tardor(asset,any)
            if int(mesf)==0:
                mes_final=1
                if int(mesi)==0:
                    mes_inici=1
                else:
                    mes_inici=int(mesi)        
                data_inici = datetime.datetime(2019,month=mes_inici, day=int(diai))
                data_final = datetime.datetime(2020,month=mes_final, day=int(diaf))
                '''elif int(mesi)==0:
                data_inici = datetime.datetime(2020,month=1, day=int(diai))
                data_final = datetime.datetime(2019,month=int(mesf), day=int(diaf))'''
            else:
                data_inici = datetime.datetime(2019,month=int(mesi), day=int(diai))
                data_final = datetime.datetime(2019,month=int(mesf), day=int(diaf))
            start_fall.append(data_inici)
            end_fall.append(data_final)
            yearsi.append(any)
            yearsf.append(any)

            if len(y)==len(colorsT(asset,any)):
                c=colorsT(asset,any)
            else:
                c='blue'

            plt.scatter(x, y, c=c, s=5)

    print(end_fall)
    start_fall = mdates.date2num(start_fall)
    end_fall = mdates.date2num(end_fall)
    yearsi = np.array(yearsi, dtype=float)
    yearsf = np.array(yearsf, dtype=float)
    print(yearsf)
    print(end_fall)

    # Ajustar líneas de tendencia utilizando regresión lineal
    start_trend = np.polyfit(yearsi, start_fall, 1)
    end_trend = np.polyfit(yearsf, end_fall, 1)

    start_slope, start_intercept = start_trend
    end_slope, end_intercept = end_trend

    # Calcular los valores predichos para las líneas de tendencia
    start_trend_line = np.polyval(start_trend, yearsi)
    end_trend_line = np.polyval(end_trend, yearsf)

    print("Ecuación de la línea de tendencia (Inicio): y = {}x + {}".format(start_slope, start_intercept))
    print("Ecuación de la línea de tendencia (Fin): y = {}x + {}".format(end_slope, end_intercept))
    print(f"nombre de dies augment inici: {start_slope*10}")
    print(f"nombre de dies augment final: {end_slope*10}")
    
    # Graficar las líneas de tendencia
    plt.plot(yearsi, start_trend_line, 'black', label='Línea de Tendencia (Inicio)')
    plt.plot(yearsf, end_trend_line, 'black', label='Línea de Tendencia (Fin)')

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


    #plt.savefig(asset+'tardor.png')