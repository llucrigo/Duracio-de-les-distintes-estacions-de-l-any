#Diccionari de temperatures màximes i mínimes a les estacions de Balears

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, FuncFormatter
import pytz
from sklearn.linear_model import LinearRegression

#Definim una funció que ens torni el valor mitjà de l'inici i el final de la primavera dels darrers 30 anys.

def mitjanaTmaxH(asset):
#Cream un bucle que ens guardi els noms de les columnes que necessitarem

    columnes_inici_hivern = []
    columnes_final_hivern = []
    ci=1993
    i=0

    while i<30:
        columnes_inici_hivern.append(str(ci+i)+'12')
        columnes_final_hivern.append(str(ci+i)+'3')
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

    # Seleccionar columnes per agafar només les del mes de desembre (inici hivern)
    columnes_seleccionades_ih = df[columnes_inici_hivern]

    # Seleccionar columnes per agafar només les del mes de març (final hivern)
    columnes_seleccionades_fh = df[columnes_final_hivern]

    # Calcular la mitjana dels elements (Temperatura màxima mitjana de l'inici de l'hivern)
    mitjana_ih = np.nanmean(columnes_seleccionades_ih)
    # Calcular la mitjana dels elements (Temperatura màxima mitjana del final de l'hivern)
    mitjana_fh = np.nanmean(columnes_seleccionades_fh)


    # Imprimir la media
    #print(mitjana_ih)
    #print(mitjana_fh)

    return mitjana_ih, mitjana_fh

'''
print("Lluc:")
mitjanaTmaxH('B013-Lluc-TMAX.xlsx')
print("Port:")
mitjanaTmaxH('B228-Portopí-TMAX.xlsx')
print("Cabaneta:")
mitjanaTmaxH('B273-La-Cabaneta-TMAX.xlsx')
print("Aeroport:")
print(mitjanaTmaxH('B278-Palma-Aeropuerto-TMAX.xlsx'))
print("Capdepera:")
mitjanaTmaxH('B569X-Faro-Capdepera-TMAX.xlsx')
print("S'albufera:")
mitjanaTmaxH('B605-Muro-S-Albufera-TMAX.xlsx')
print("Menorca")
mitjanaTmaxH('B893-Menorca-Aeropuerto-TMAX.xlsx')
print("Eivissa:")
mitjanaTmaxH('B954-Ibiza-Aeropuerto-TMAX.xlsx')
'''

def inici_hivern(asset, any):
    #L'inici de l'hivern coincideix amb el final de la tardor
    requisit, requisitf = mitjanaTmaxH(asset)  # Requisito común a verificar
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

    columnes_seleccionades_fh = df_invertido_final[[str(any+1)+'0', str(any)+'12', str(any)+'11', str(any)+'10', str(any)+'9']]
    #print(columnes_seleccionades_ie)
    final_df = pd.DataFrame(columnes_seleccionades_fh)
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
                #print(f"final hivern any {any}:")
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


m=inici_hivern('B278-Palma-Aeropuerto-TMAX.xlsx',2003)
#print(m)

def final_hivern(asset, any):
    #El final de l'hivern coincideix amb l'inici de la primavera

    requisit, requisitf = mitjanaTmaxH(asset)  # Requisito común a verificar
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

    columnes_seleccionades_ih = df[[str(any+1)+'2', str(any+1)+'3', str(any+1)+'4', str(any+1)+'5']]
    #print(columnes_seleccionades_ih)
    inici_df = pd.DataFrame(columnes_seleccionades_ih)
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
                #print(f"inici hivern any {any}:")
                #print(elements_cumpleixen_requisit_inici[0])

                numero=elements_cumpleixen_requisit_inici[0]

                any = numero[:4]
                mes = numero[4]
                dia = numero[5:]

                return any, mes, dia
            
    return None
                
                
f=final_hivern('B278-Palma-Aeropuerto-TMAX.xlsx',2003)
#print(f)

def arrays_graficaH(asset, any):
    #print(inici_hivern(asset, any))
    print(final_hivern(asset, any))
    if inici_hivern(asset, any)==None:
        f=final_hivern(asset, any)
        if f==None:
            array_y=datetime.datetime(2020, 1, 30)
            array_x = any + 1
            c='green'
            return c, array_y, array_x
        
        else:
            anyf, mesf, diaf = final_hivern(asset, any)
            if int(mesf) == 0:
                array_y=datetime.datetime(2020, month=1, day=int(diaf))
            else:
                array_y=datetime.datetime(2020, month=int(mesf), day=int(diaf)) #com que es el final de s'hivern acabara l'any següent si o si
            array_x = anyf
            c='red'
            return c, array_y, array_x    

    elif final_hivern(asset, any)==None:
        i=inici_hivern(asset, any)
        if i==None:
            array_y=datetime.datetime(2020, 1, 30)
            array_x = any + 1
            c='green'
            return c, array_y, array_x
        else:
            anyi, mesi, diai = inici_hivern(asset, any)
            if int(mesi)==0:
                array_y=datetime.datetime(2020, month=1, day=int(diai))
            elif int(mesi)==12 or int(mesi)==11:
                array_y=datetime.datetime(2019, month=int(mesi), day=int(diai))
            else:
                array_y=datetime.datetime(2020, month=int(mesi), day=int(diai))
            array_x = any + 1
            c='red'
            return c, array_y, array_x

    else:           
        #Cream l'array de dates (l'any que inclourem serà aleatori perquè després farem un altre llista per etiquetar els anys)
        anyi, mesi, diai = inici_hivern(asset, any)
        #print(inici_hivern(asset, any))

        anyf, mesf, diaf = final_hivern(asset, any)
        #print(final_hivern(asset, any))

        if int(mesi)==0:
            mes_inici=1
            if int(mesf)==0:
                mes_final=1
            else:
                mes_final=int(mesf)
            data_inici = datetime.datetime(2020,month=mes_inici, day=int(diai))
            data_final = datetime.datetime(2020,month=mes_final, day=int(diaf))
        elif int(mesf)==0:
            data_inici = datetime.datetime(2019,month=int(mesi), day=int(diai))
            data_final = datetime.datetime(2020,month=1, day=int(diaf))
        elif int(mesi)==12 or int(mesi)==11:
            data_inici = datetime.datetime(2019,month=int(mesi), day=int(diai))
            data_final = datetime.datetime(2020,month=int(mesf), day=int(diaf))
        else:
            data_inici = datetime.datetime(2020,month=int(mesi), day=int(diai))
            data_final = datetime.datetime(2020,month=int(mesf), day=int(diaf))             

        # Calcula la cantidad de días entre la fecha de inicio y la fecha de fin
        num_dias = (data_final - data_inici).days + 1

        # Genera un array de fechas utilizando un bucle for
        array_y = [data_inici + datetime.timedelta(days=i) for i in range(num_dias)]
        array_x = np.full(len(array_y), anyf)
        #print(array_y)
        #print(array_x)
        #print(len(array_y))
        #print(len(array_x))
        return array_y, array_x, data_inici, data_final, anyf


def colorsH(asset, any):

    requisit, requisitf = mitjanaTmaxH(asset)

    anyi, mesi, diai = inici_hivern(asset, any)
    anyf, mesf, diaf = final_hivern(asset, any)

    j=int(mesf)

    if int(mesi)==0:
        i=int(mesi)+1
    elif int(mesi)==12:
        i=0
    elif int(mesi)==11:
        i=-1
    else:
        i = int(mesi)

    if int(mesf)==0:
        j=1

    columnes = []

    while i <= j:
        if i==1:
            columnes.append(str(any+1)+"0")
        elif i==0:
            columnes.append(str(any)+"12")
        elif i==-1:
            columnes.append(str(any)+"11")
        else:
            columnes.append(str(any+1)+str(i))
        i = i+1

    #print(columnes)
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
    df.loc[30, str(any+1)+'6'] = 'None'
    df.loc[30, str(any+1)+'4'] = 'None'
    df.loc[30, str(any+1)+'2'] = 'None'
    df.loc[29, str(any+1)+'2'] = 'None'
    df.loc[30, str(any)+'9'] = 'None'
    df.loc[30, str(any)+'11'] = 'None'

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

'''inici_hivern('B278-Palma-Aeropuerto-TMAX.xlsx',2020)
final_hivern('B278-Palma-Aeropuerto-TMAX.xlsx',2020)
arrays_graficaH('B278-Palma-Aeropuerto-TMAX.xlsx',2020)
colorsH('B278-Palma-Aeropuerto-TMAX.xlsx',2020)'''



def y_formatter(value, _):
    fecha = datetime.datetime.fromordinal(int(value) + datetime.datetime(2000, 1, 1).toordinal()+1)
    return fecha.strftime("%m-%d")


def grafica_hivern(asset, anyi, anyf):
    requisit, requisitf = mitjanaTmaxH(asset)
    yearsf = []
    yearsi = []
    start_summer=[]
    end_summer=[]
    for any in range(anyi,anyf):
        
        if inici_hivern(asset, any) is None: 
            yearsf.append(any+1)
            c, y, x=arrays_graficaH(asset,any)
            end_summer.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c=c, s=5)

        elif final_hivern(asset, any) is None:
            yearsi.append(any+1)
            c, y, x=arrays_graficaH(asset,any)
            start_summer.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c=c, s=5)

        else:
            y, x, data_inici, data_final, any_final = arrays_graficaH(asset, any)
            start_summer.append(data_inici)
            end_summer.append(data_final)
            yearsf.append(any+1)
            yearsi.append(any+1)

            if len(y)==len(colorsH(asset,any)):
                c=colorsH(asset,any)
            else:
                c='blue'
            y=mdates.date2num(y)
            x = np.array(x, dtype=float)
            plt.scatter(x, y, c=c, s=5)

    print(end_summer)
    start_summer = mdates.date2num(start_summer)
    end_summer = mdates.date2num(end_summer)
    yearsi = np.array(yearsi, dtype=float)
    yearsf = np.array(yearsf, dtype=float)
    print(yearsf)

    print(end_summer)
    # Ajustar líneas de tendencia utilizando regresión lineal
    start_trend = np.polyfit(yearsi, start_summer, 1)
    end_trend = np.polyfit(yearsf, end_summer, 1)

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
    #plt.show()

    plt.xlabel('any', fontsize=12)
    plt.ylabel('mes-dia', fontsize=12)



#grafica_hivern('B278-Palma-Aeropuerto-TMAX.xlsx', 1975, 2023)
