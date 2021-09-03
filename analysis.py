import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes, plot_windrose
import os
import numpy as np

current_dir = os.getcwd()
days_dir = current_dir + '/wrf/'

#%%
################
# Obtención día
################
def get_day():
    available_days = []

    for day in os.listdir(days_dir):
        available_days.append(day)

    print('Los días disponibles son: {}\n'.format(available_days))
    day = input('Introduce el día a analizar [dd-mm-YYYY]: ')

    if day in available_days:

        return day
    else:
        print('El directorio {} no existe'.format(day))
        return None

#%%
###############################
# Obtención de datos de viento
###############################
def data_extraction(day):
    is_wrf = False
    is_real = False

    file_dir = days_dir + day

    for file in os.listdir(file_dir):
        if file.startswith('Horario') and file.endswith('.txt') and '10min' not in file:

            df_wrf = pd.read_csv(file_dir + '/' + file)
            df_wrf = df_wrf[df_wrf['Fecha'] == day]

            # Primera fecha de archivo wrf
            day_wrf = df_wrf.iloc[0, 0]
            if day_wrf == day:
                is_wrf = True
            else:
                print('El archivo {} no contiene datos del dia seleccionado [{}]'.format(file, day))
                pass

        elif file == 'concodiro.xlsx':

            df_real = pd.read_excel(file_dir + '/concodiro.xlsx')

            # Primera fecha de archivo estación meteorologica
            day_real = (((df_real.iloc[2, 1]._date_repr)).split('-'))
            day_real.reverse()
            day_real = '-'.join(day_real)
            if day_real == day:
                is_real = True
            else:
                print('El archivo {} no contiene datos del dia seleccionado [{}]'.format(file, day))
                pass

    if is_wrf and is_real:
        print('Se han encontrado archivos compatibles\n')
        return df_real, df_wrf

    else:
        print('No se han encontrado archivos compatibles\n')
        return None, None

#%%
#################################
# Generacion de dataframe propio
#################################
def get_wind(df_real, df_wrf):
    try:

        WD_real = df_real.iloc[2:, 4]
        WD_real.name = 'WD_real'
        WD_real.reset_index(drop=True, inplace=True)

        WS_real = df_real.iloc[2:, 3]
        WS_real.name = 'WS_real'
        WS_real.reset_index(drop=True, inplace=True)

        WD_wrf = df_wrf.iloc[0:, 3]
        WD_wrf.name = 'WD_wrf'
        WD_real.reset_index(drop=True, inplace=True)

        WS_wrf = df_wrf.iloc[0:, 2]
        WS_wrf.name = 'WS_wrf'
        WS_wrf.reset_index(drop=True, inplace=True)

        day_wrf = df_wrf.iloc[0:, 0]
        day_wrf.name = 'day'
        day_wrf.reset_index(drop=True, inplace=True)

        hour = df_wrf.iloc[0:, 1]
        hour.reset_index(drop=True, inplace=True)
        hour.name = 'hour'

        df_data = pd.concat([day_wrf, hour, WD_real, WS_real, WD_wrf, WS_wrf], axis=1)
        print(df_data)

        return df_data

    except Exception:
        return None

#%%
##################################################
# Genera histograma radial del registro completo
##################################################
def total_windrose(df_data, day):
    df_data = df_data.loc[df_data['day'] == day]

    fig = plt.figure(day)

    W_real = fig.add_subplot(121, projection='windrose')
    plt.title('Wind real')
    W_real.bar(df_data.iloc[:, 2], df_data.iloc[:, 3], normed=True, opening=0.8, edgecolor='white')
    W_real.set_legend()

    W_wrf = fig.add_subplot(122, projection='windrose')
    plt.title('Wind wrf')
    W_wrf.bar(df_data.iloc[:, 4], df_data.iloc[:, 5], normed=True, opening=0.8, edgecolor='white')
    W_wrf.set_legend()

    plt.show()

#%%
####################################################################
# Generacion de histograma radial para cada hora entre 12:00 y 20:00
####################################################################
def hour_windrose(df_data, day):
    print('\nComprobacion horaria \n')
    #hour = input('Introduce la hora a comprobar (hh:00): ')
    hours = ['12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00']

    i = 1
    fig = plt.figure( '{}'.format(day))

    for hour in hours:

        W_hour = df_data.loc[df_data['hour'] == hour]

    
        W_hour_real = fig.add_subplot(3, 6, i, projection='windrose')
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=0.55)
        plt.title(day + '\nW real histograma de {}'.format(hour))
        W_hour_real.bar(W_hour.iloc[:, 2], W_hour.iloc[:, 3], normed=True, opening=0.8, edgecolor='white')
        #W_hour_real.set_legend()

        i += 1

        W_hour_pred = fig.add_subplot(3, 6, i, projection='windrose')
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=0.55)
        plt.title(day + '\nW pred histograma de {}'.format(hour))
        W_hour_pred.bar(W_hour.iloc[:, 4], W_hour.iloc[:, 5], normed=True, opening=0.8, edgecolor='white')
        #W_hour_pred.set_legend()

        i += 1

    plt.show()


#%%
def main():
    day = get_day()
    df_real, df_wrf = data_extraction(day)
    df_data = get_wind(df_real, df_wrf)
    if not df_data.empty:
        total_windrose(df_data, day)
        hour_windrose(df_data, day)
    else:
        print('No se pueden mostrar las direcciones del viento')
        pass


if __name__ == '__main__':
    main()
