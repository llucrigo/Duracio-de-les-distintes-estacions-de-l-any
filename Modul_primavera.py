#Diccionari de temperatures màximes i mínimes a les estacions de Balears

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, FuncFormatter

#Definim una funció que ens torni el valor mitjà de l'inici i el final de la primavera dels darrers 30 anys.

def mitjanaTmaxP(asset):
#Cream un bucle que ens guardi els noms de les columnes que necessitarem

    columnes_inici_primavera = []
    columnes_final_primavera = []
    ci=1993
    i=0

    while i<30:
        columnes_inici_primavera.append(str(ci+i)+'3')
        columnes_final_primavera.append(str(ci+i)+'6')
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

    # Seleccionar columnes per agafar només les del mes de març (inici primavera)
    columnes_seleccionades_ip = df[columnes_inici_primavera]

    # Seleccionar columnes per agafar només les del mes de juny (final primavera)
    columnes_seleccionades_fp = df[columnes_final_primavera]

    # Calcular la mitjana dels elements (Temperatura màxima mitjana de l'inici de la primavera)
    mitjana_ip = np.nanmean(columnes_seleccionades_ip)
    # Calcular la mitjana dels elements (Temperatura màxima mitjana del final de la primavera)
    mitjana_fp = np.nanmean(columnes_seleccionades_fp)


    # Imprimir la media
    #print(mitjana_ip)
    #print(mitjana_fp)

    return mitjana_ip, mitjana_fp

'''
print("Lluc:")
mitjanaTmaxP('B013-Lluc-TMAX.xlsx')
print("Port:")
mitjanaTmaxP('B228-Portopí-TMAX.xlsx')
print("Cabaneta:")
mitjanaTmaxP('B273-La-Cabaneta-TMAX.xlsx')
print("Aeroport:")
print(mitjanaTmaxP('B278-Palma-Aeropuerto-TMAX.xlsx'))
print("Capdepera:")
mitjanaTmaxP('B569X-Faro-Capdepera-TMAX.xlsx')
print("S'albufera:")
mitjanaTmaxP('B605-Muro-S-Albufera-TMAX.xlsx')
print("Menorca")
mitjanaTmaxP('B893-Menorca-Aeropuerto-TMAX.xlsx')
print("Eivissa:")
mitjanaTmaxP('B954-Ibiza-Aeropuerto-TMAX.xlsx')
'''

def inici_primavera(asset, any):
    #Hem de fer dataframes que recoeixin les dades compreses entre gener i maig de cada any

    requisit, requisitf = mitjanaTmaxP(asset)  # Requisito común a verificar
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

    columnes_seleccionades_ip = df[[str(any)+'2', str(any)+'3', str(any)+'4', str(any)+'5']]
    #print(columnes_seleccionades_ip)
    inici_df = pd.DataFrame(columnes_seleccionades_ip)
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
                #print(f"inici primavera any {any}:")
                #print(elements_cumpleixen_requisit_inici[0])

                numero=elements_cumpleixen_requisit_inici[0]

                any = numero[:4]
                mes = numero[4]
                dia = numero[5:]

                return any, mes, dia
            
    return None


m=inici_primavera('B278-Palma-Aeropuerto-TMAX.xlsx',2003)
#print(m)

def final_primavera(asset, any):
    #Hem de fer dataframes que recoeixin les dades compreses entre abril i juny de cada any

    requisit, requisitf = mitjanaTmaxP(asset)  # Requisito común a verificar
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

            if elemento >= requisitf:
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
                
                
f=final_primavera('B278-Palma-Aeropuerto-TMAX.xlsx',2003)
#print(f)

def arrays_graficaP(asset, any):
    print(inici_primavera(asset, any))
    if inici_primavera(asset, any)==None:
        f=final_primavera(asset, any)
        if f==None:
            array_y=datetime.datetime(2020, 4, 30)
            array_x = any
            c='green'
            return c, array_y, array_x
        
        else:
            anyf, mesf, diaf = final_primavera(asset, any)
            if int(mesf) == 0:
                array_y=datetime.datetime(2020, month=1, day=int(diaf))
            else:
                array_y=datetime.datetime(2020, month=int(mesf), day=int(diaf))
            array_x = any
            c='red'
            return c, array_y, array_x    

    elif final_primavera(asset, any)==None:
        i=inici_primavera(asset, any)
        if i==None:
            array_y=datetime.datetime(2020, 4, 30)
            array_x = any
            c='green'
            return c, array_y, array_x
        else:
            anyi, mesi, diai = inici_primavera(asset, any)
            if mesi==0:
                array_y=datetime.datetime(2020, month=1, day=int(diai))
            else:
                array_y=datetime.datetime(2020, month=int(mesi), day=int(diai))
            array_x = any
            c='red'
            return c, array_y, array_x

    else:           
        #Cream l'array de dates (l'any que inclourem serà aleatori perquè després farem un altre llista per etiquetar els anys)
        anyi, mesi, diai = inici_primavera(asset, any)
        #print(inici_primavera(asset, any))

        anyf, mesf, diaf = final_primavera(asset, any)
        #print(final_primavera(asset, any))

        if int(mesi)==0:
            data_inici = datetime.datetime(2020,month=1, day=int(diai))
            data_final = datetime.datetime(2020,month=int(mesf), day=int(diaf))
        elif int(mesf)==0:
            data_inici = datetime.datetime(2020,month=int(mesi), day=int(diai))
            data_final = datetime.datetime(2020,month=1, day=int(diaf))
        else:
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


def colorsP(asset, any):

    requisit, requisitf = mitjanaTmaxP(asset)

    anyi, mesi, diai = inici_primavera(asset, any)
    anyf, mesf, diaf = final_primavera(asset, any)

    if int(mesi)==0:
        i=int(mesi)+1
    else:
        i = int(mesi)

    columnes = []

    while i <= int(mesf):
        if i==1:
            columnes.append(str(any)+"0")
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
    df.loc[30, str(any)+'4'] = 'None'
    df.loc[30, str(any)+'2'] = 'None'
    df.loc[29, str(any)+'2'] = 'None'

    # Seleccionar columnes per agafar només les de l'interval
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
                if value < requisit:
                    color.append('green')
                else:
                    color.append('red')
            else:
                color.append('white')

    #print(color)
    #print(len(color))
    return color
'''
inici_primavera('B278-Palma-Aeropuerto-TMAX.xlsx',2020)
final_primavera('B278-Palma-Aeropuerto-TMAX.xlsx',2020)
arrays_graficaP('B278-Palma-Aeropuerto-TMAX.xlsx',2020)
colorsP('B278-Palma-Aeropuerto-TMAX.xlsx',2020)'''

def y_formatter(value, _):
    fecha = datetime.datetime.fromordinal(int(value) + datetime.datetime(2000, 1, 1).toordinal()+1)
    return fecha.strftime("%m-%d")


def grafica_primavera(asset, anyi, anyf):
    requisit, requisitf = mitjanaTmaxP(asset)
    yearsf = []
    yearsi= []
    start_spring=[]
    end_spring=[]
    for any in range(anyi,anyf):
        if inici_primavera(asset, any) is None and final_primavera(asset, any) is None:
            c, y, x=arrays_graficaP(asset,any)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c=c, s=5)
        elif inici_primavera(asset, any) is None: 
            yearsf.append(any)
            c, y, x=arrays_graficaP(asset,any)
            end_spring.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c=c, s=5)

        elif final_primavera(asset, any) is None:
            yearsi.append(any)
            c, y, x=arrays_graficaP(asset,any)
            start_spring.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c=c, s=5)

        else:
            y, x=arrays_graficaP(asset,any)

            anyi, mesi, diai = inici_primavera(asset,any)
            anyf, mesf, diaf = final_primavera(asset,any)
            if int(mesi)==0:
                data_inici = datetime.datetime(2020,month=1, day=int(diai))
                data_final = datetime.datetime(2020,month=int(mesf), day=int(diaf))
            elif int(mesf)==0:
                data_inici = datetime.datetime(2020,month=int(mesi), day=int(diai))
                data_final = datetime.datetime(2020,month=1, day=int(diaf))
            else:
                data_inici = datetime.datetime(2020,month=int(mesi), day=int(diai))
                data_final = datetime.datetime(2020,month=int(mesf), day=int(diaf))
            start_spring.append(data_inici)
            end_spring.append(data_final)
            yearsi.append(any)
            yearsf.append(any)

            if len(y)==len(colorsP(asset,any)):
                c=colorsP(asset,any)
            else:
                c='blue'

            plt.scatter(x, y, c=c, s=5)
    print(start_spring)
    start_spring = mdates.date2num(start_spring)
    end_spring = mdates.date2num(end_spring)
    print(start_spring)
    print(yearsi)

    # Ajustar líneas de tendencia utilizando regresión lineal
    start_trend = np.polyfit(yearsi, start_spring, 1)
    end_trend = np.polyfit(yearsf, end_spring, 1)

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

    #plt.show()
    #plt.savefig(asset+'primavera.png')