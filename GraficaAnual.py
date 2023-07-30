#Prova grafica anual
from Modul_hivern import *
from Modul_estiu import *
from Modul_primavera import *
from Modul_tardor import *

def grafica_E(asset, anyi, anyf):
    requisit, requisitf = mitjanaTmaxE(asset)
    yearsi = []
    yearsf = []
    start_summer=[]
    end_summer=[]
    llegenda = 'Estiu'

    for any in range(anyi,anyf):
        
        if inici_estiu(asset, any) is None and final_estiu(asset, any) is None:
            c, y, x=arrays_graficaE(asset,any)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c='gold', s=5)
        elif inici_estiu(asset, any) is None: 
            yearsf.append(any)
            c, y, x=arrays_graficaE(asset,any)
            end_summer.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c='gold', s=5)

        elif final_estiu(asset, any) is None:
            yearsi.append(any)
            c, y, x=arrays_graficaE(asset,any)
            start_summer.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c='gold', s=5)

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

            plt.scatter(x, y, c='gold', s=2, label = llegenda)

        llegenda=''

    start_summer = mdates.date2num(start_summer)
    end_summer = mdates.date2num(end_summer)

    # Ajustar líneas de tendencia utilizando regresión lineal
    start_trend = np.polyfit(yearsi, start_summer, 1)
    end_trend = np.polyfit(yearsf, end_summer, 1)

    # Calcular los valores predichos para las líneas de tendencia
    start_trend_line = np.polyval(start_trend, yearsi)
    end_trend_line = np.polyval(end_trend, yearsf)

    # Graficar las líneas de tendencia
    plt.plot(yearsi, start_trend_line, 'black')
    plt.plot(yearsf, end_trend_line, 'black')

    plt.gca().yaxis.set_major_formatter(FuncFormatter(y_formatter))

    plt.title(asset)

    # Configurar los ticks en el eje X para que aparezcan cada dos años
    plt.gca().xaxis.set_major_locator(MultipleLocator(base=2))

    # Configurar los ticks en el eje Y para que aparezcan cada 4 dias
    plt.gca().yaxis.set_major_locator(MultipleLocator(base=15))

    plt.xticks(rotation=90)

def grafica_H(asset, anyi, anyf):
    requisit, requisitf = mitjanaTmaxH(asset)
    yearsi = []
    yearsf = []
    start_summer=[]
    end_summer=[]
    llegenda = 'Hivern'

    for any in range(anyi,anyf):
        
        if inici_hivern(asset, any) is None: 
            yearsf.append(any+1)
            c, y, x=arrays_graficaH(asset,any)
            end_summer.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c='cornflowerblue', s=5)

        elif final_hivern(asset, any) is None:
            yearsi.append(any+1)
            c, y, x=arrays_graficaH(asset,any)
            start_summer.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c='cornflowerblue', s=5)

        else:
            y, x, data_inici, data_final, any_final = arrays_graficaH(asset, any)
            start_summer.append(data_inici)
            end_summer.append(data_final)
            yearsi.append(any+1)
            yearsf.append(any+1)

            y=mdates.date2num(y)
            x = np.array(x, dtype=float)
            plt.scatter(x, y, c='cornflowerblue', s=2, label = llegenda)
        llegenda=''


    start_summer = mdates.date2num(start_summer)
    end_summer = mdates.date2num(end_summer)
    yearsi = np.array(yearsi, dtype=float)
    yearsf = np.array(yearsf, dtype=float)

    # Ajustar líneas de tendencia utilizando regresión lineal
    start_trend = np.polyfit(yearsi, start_summer, 1)
    end_trend = np.polyfit(yearsf, end_summer, 1)

    # Calcular los valores predichos para las líneas de tendencia
    start_trend_line = np.polyval(start_trend, yearsi)
    end_trend_line = np.polyval(end_trend, yearsf)

    # Graficar las líneas de tendencia
    plt.plot(yearsi, start_trend_line, 'black')
    #plt.plot(years, end_trend_line, 'black')

    plt.gca().yaxis.set_major_formatter(FuncFormatter(y_formatter))

    plt.title(asset)

    # Configurar los ticks en el eje X para que aparezcan cada dos años
    plt.gca().xaxis.set_major_locator(MultipleLocator(base=2))

    # Configurar los ticks en el eje Y para que aparezcan cada 4 dias
    plt.gca().yaxis.set_major_locator(MultipleLocator(base=15))

    plt.xticks(rotation=90)
    #plt.show()

def grafica_P(asset, anyi, anyf):
    requisit, requisitf = mitjanaTmaxP(asset)
    yearsf = []
    yearsi= []
    start_spring=[]
    end_spring=[]
    llegenda = 'Primavera'

    for any in range(anyi,anyf):
        if inici_primavera(asset, any) is None and final_primavera(asset, any) is None:
            c, y, x=arrays_graficaP(asset,any)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c='yellowgreen', s=5)
        elif inici_primavera(asset, any) is None: 
            yearsf.append(any)
            c, y, x=arrays_graficaP(asset,any)
            end_spring.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c='yellowgreen', s=5)

        elif final_primavera(asset, any) is None:
            yearsi.append(any)
            c, y, x=arrays_graficaP(asset,any)
            start_spring.append(y)
            x = np.array(x, dtype=float)
            y=mdates.date2num(y)
            plt.scatter(x, y, c='yellowgreen', s=5)

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

            plt.scatter(x, y, c='yellowgreen', s=2, label = llegenda)

        llegenda=''

    start_spring = mdates.date2num(start_spring)
    end_spring = mdates.date2num(end_spring)

    # Ajustar líneas de tendencia utilizando regresión lineal
    start_trend = np.polyfit(yearsi, start_spring, 1)
    #end_trend = np.polyfit(yearsf, end_spring, 1)

    # Calcular los valores predichos para las líneas de tendencia
    start_trend_line = np.polyval(start_trend, yearsi)
    #end_trend_line = np.polyval(end_trend, yearsf)

    # Graficar las líneas de tendencia
    plt.plot(yearsi, start_trend_line, 'black')
    #plt.plot(yearsf, end_trend_line, 'black')

    plt.gca().yaxis.set_major_formatter(FuncFormatter(y_formatter))

    plt.grid()
    plt.title(asset)

    # Configurar los ticks en el eje X para que aparezcan cada dos años
    plt.gca().xaxis.set_major_locator(MultipleLocator(base=2))

    # Configurar los ticks en el eje Y para que aparezcan cada 4 dias
    plt.gca().yaxis.set_major_locator(MultipleLocator(base=15))

    plt.xticks(rotation=90)

def grafica_T(asset, anyi, anyf):
    requisit, requisitf = mitjanaTmaxT(asset)
    yearsi = []
    yearsf = []
    start_fall=[]
    end_fall=[]
    llegenda = 'Tardor'

    for any in range(anyi,anyf):
        
        if inici_tardor(asset, any) is None:
            c, y, x=arrays_graficaT(asset,any)
            end_fall.append(y)
            yearsf.append(any)
            plt.scatter(x, y, c='darkgoldenrod', s=5)

        elif final_tardor(asset, any) is None:
            c, y, x=arrays_graficaT(asset,any)
            start_fall.append(y)
            yearsi.append(any)
            plt.scatter(x, y, c='darkgoldenrod', s=5)

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

            plt.scatter(x, y, c='darkgoldenrod', s=2, label = llegenda)
        llegenda = ''


    start_fall = mdates.date2num(start_fall)
    end_fall = mdates.date2num(end_fall)
    yearsi = np.array(yearsi, dtype=float)
    yearsf = np.array(yearsf, dtype=float)

    # Ajustar líneas de tendencia utilizando regresión lineal
    start_trend = np.polyfit(yearsi, start_fall, 1)
    #end_trend = np.polyfit(yearsf, end_fall, 1)

    # Calcular los valores predichos para las líneas de tendencia
    start_trend_line = np.polyval(start_trend, yearsi)
    #end_trend_line = np.polyval(end_trend, yearsf)

    # Graficar las líneas de tendencia
    plt.plot(yearsi, start_trend_line, 'black')
    #plt.plot(yearsf, end_trend_line, 'black')

    plt.gca().yaxis.set_major_formatter(FuncFormatter(y_formatter))

    plt.grid()
    plt.title(asset)

    # Configurar los ticks en el eje X para que aparezcan cada dos años
    plt.gca().xaxis.set_major_locator(MultipleLocator(base=2))

    # Configurar los ticks en el eje Y para que aparezcan cada 4 dias
    plt.gca().yaxis.set_major_locator(MultipleLocator(base=15))

    plt.xticks(rotation=90)

'''grafica_H('B278-Palma-Aeropuerto-TMAX.xlsx', 1975, 2022)
grafica_P('B278-Palma-Aeropuerto-TMAX.xlsx', 1976, 2023)
grafica_E('B278-Palma-Aeropuerto-TMAX.xlsx', 1976, 2023)
grafica_T('B278-Palma-Aeropuerto-TMAX.xlsx', 1976, 2023)
plt.legend(loc='upper left')
plt.show()'''

grafica_H('B908-Sant-Joan-de-Labritja-TMAX.xlsx', 1993, 2023)
grafica_P('B908-Sant-Joan-de-Labritja-TMAX.xlsx', 1994, 2024)
grafica_E('B908-Sant-Joan-de-Labritja-TMAX.xlsx', 1993, 2023)
grafica_T('B908-Sant-Joan-de-Labritja-TMAX.xlsx', 1993, 2023)
plt.legend(loc='upper left')

plt.xlabel('any', fontsize=12)
plt.ylabel('mes-dia', fontsize=12)

plt.show()