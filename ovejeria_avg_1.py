import math

import numpy
import pandas
import tqdm as tqdm
from netCDF4 import Dataset

import wrf
import sys

ncfile = Dataset(sys.argv[1])
#ncfile = Dataset('wrf\wrfout_d03_2021-05-27_00_00_00')

rainnc = wrf.getvar(ncfile, "RAINNC", wrf.ALL_TIMES)
rainc = wrf.getvar(ncfile, "RAINC", wrf.ALL_TIMES)
v10 = wrf.getvar(ncfile, "V10", wrf.ALL_TIMES)
u10 = wrf.getvar(ncfile, "U10", wrf.ALL_TIMES)
t2 = wrf.getvar(ncfile, "T2", wrf.ALL_TIMES)
rh2 = wrf.getvar(ncfile, "rh2", wrf.ALL_TIMES)
z = wrf.getvar(ncfile, "z")

length = v10.sizes['Time']

rainT_0 = 0

t0 = pandas.to_datetime(wrf.extract_times(ncfile, 0))

txtfile = open('C:\\Users\\Usuario\\Documents\\ALBERTO_Local\\02_Proyectos\\CODELCO\\02_DESEMPEÑO\\WD_Calcs\\wrf\\Horario_{:0>2d}-{:0>2d}-{:d}.txt'.format(t0.day, t0.month, t0.year), "w")
txtfile.write("Fecha,Hora,Vel. Viento (km/h),Direccion Viento,Direccion Viento (letra),Precipitacion (mm),Temperatura,HR,Riesgo\r\n")

txt2file = open('C:\\Users\\Usuario\\Documents\\ALBERTO_Local\\02_Proyectos\\CODELCO\\02_DESEMPEÑO\\WD_Calcs\\wrf\\Pronostico_{:0>2d}-{:0>2d}-{:d}.txt'.format(t0.day, t0.month, t0.year), "w")
txt2file.write("Fecha,Vel. Viento (km/h),Precipitacion (mm),Riesgo,T max,T min,HR media\r\n")

txt3file = open('C:\\Users\\Usuario\\Documents\\ALBERTO_Local\\02_Proyectos\\CODELCO\\02_DESEMPEÑO\\WD_Calcs\\wrf\\Horario_10min_{:0>2d}-{:0>2d}-{:d}.txt'.format(t0.day, t0.month, t0.year), "w")
txt3file.write("Fecha,Hora,Vel. Viento (m/s),Direccion Viento\r\n")

fila_i = 19
fila_f = 21+1

col_i = 21
col_f = 23+1

max_speed = 0
rain_t = 0
risk_speed = 0
max_temp = -273
min_temp = 100
avg_rh = 0

altura_estacion = 640
capa_dir = 3

t00 = pandas.to_datetime(wrf.extract_times(ncfile, 0)).tz_localize('UTC').tz_convert('America/Santiago')
tend = pandas.to_datetime(wrf.extract_times(ncfile, length-1)).tz_localize('UTC').tz_convert('America/Santiago')
hoy = pandas.to_datetime("today")
hoy = hoy.replace(hour=0,minute=0,second=0,microsecond=0)
hoy = hoy.tz_localize('America/Santiago')

for i in range(0, length, 6):
	print('{}/{}'.format(i, length))

	t = pandas.to_datetime(wrf.extract_times(ncfile, i)).tz_localize('UTC').tz_convert('America/Santiago')

	if (t.day == t00.day and t.month == t00.month) or (t.day == tend.day and t.month == tend.month):
		continue

	WS_max = 0
	WS_med = 0
	WD_med = 0
	T_med = 0
	RH_med = 0

	wdir_sin = 0
	wdir_cos = 0

	if (i + 6) < length:
		rango = i + 6
		div = 6
	else:
		rango = length - 1
		div = length - i - 1

	for j in range(i, rango):
		wind = wrf.g_uvmet.get_uvmet_wspd_wdir(ncfile, j)
		wspeed = wrf.interplevel(wind[0], z, altura_estacion)
		speed_i = wspeed[20, 21].values.item(0) * 3.6
		WS_med += speed_i
		
		for x in range(fila_f-fila_i-1):
			for y in range(col_f-col_i-1):
				wdir_j = wind[1].values[capa_dir][fila_i:fila_f, col_i:col_f][x,y]
				wspeed_j = wind[0].values[capa_dir][fila_i:fila_f, col_i:col_f][x,y]

				wdir_sin += math.sin(math.radians(wdir_j)) * wspeed_j
				wdir_cos += math.cos(math.radians(wdir_j)) * wspeed_j

		T_med += numpy.mean(t2[j, fila_i:fila_f, col_i:col_f]).values.item(0)
		RH_med += numpy.mean(rh2[j, fila_i:fila_f, col_i:col_f]).values.item(0)

		t10min = pandas.to_datetime(wrf.extract_times(ncfile,j)).tz_localize('UTC').tz_convert('America/Santiago')

		txt3file.write("{:0>2d}-{:0>2d}-{:d},{:0>2d}:{:0>2d},{:.1f},{:.0f}\r\n".format(t.day, t.month, t.year, t10min.hour, t10min.minute, (speed_i/3.6), wind[1].values[0][20,21]))

	WS_med /= div
	T_med /= div
	RH_med /= div
	print('\nWS_med = {}'.format(WS_med))
	T_med = round((T_med-273.15), 1)
	RH_med = round(RH_med, 0)

	WD_med = math.degrees(math.atan2(wdir_sin, wdir_cos)) + 45
	print('WD_med = {}\n'.format(WD_med))
	# Umbrales para determinacion riesgo
	if T_med > max_temp:
		max_temp = T_med

	if T_med < min_temp:
		min_temp = T_med

	if WD_med < 0:
		WD_med = WD_med + 360
	elif WD_med > 360:
		WD_med = WD_med - 360

	if WS_med > 40:
		lim_1 = 300
		lim_2 = 50
	elif WS_med > 30:
		lim_1 = 325 # 315
		lim_2 = 25 # 35
	else:
		lim_1 = 335 # 325
		lim_2 = 20 # 25

	if WD_med >= lim_1 or WD_med <= lim_2:
		taux = t.replace(hour=0,minute=0,second=0)
		if WS_med >= 30 and ((taux - hoy).days > 3):
			riesgo_h = "Alto"
		elif WS_med >= 20 and ((taux - hoy).days <= 3):
			riesgo_h = "Alto"
		elif WS_med >= 15 and ((taux - hoy).days > 3):
			riesgo_h = "Moderado"
		elif WS_med >= 10 and ((taux - hoy).days <= 3):
			riesgo_h = "Moderado"
		else:
			riesgo_h = "Bajo"

	else:
		riesgo_h = "Bajo"

	if t.hour >= 12 and t.hour < 20:
		if WS_med > max_speed:
			max_speed = WS_med

		avg_rh += RH_med

		if WD_med >= lim_1 or WD_med <= lim_2:
			if WS_med > risk_speed:
				risk_speed = WS_med

	if WD_med <= 22.5:
			letra_med = 'N';
	elif WD_med <= (22.5+1*45):
			letra_med = 'NE'
	elif WD_med <= (22.5+2*45):
			letra_med = 'E'
	elif WD_med <= (22.5+3*45):
			letra_med = 'SE'
	elif WD_med <= (22.5+4*45):
			letra_med = 'S'
	elif WD_med <= (22.5+5*45):
			letra_med = 'SO'
	elif WD_med <= (22.5+6*45):
			letra_med = 'O'
	elif WD_med <= (22.5+7*45):
			letra_med = 'NO'
	else:
			letra_med = 'N'

	rainc_i = rainc[rango, 19, 22]
	rainnc_i = rainnc[rango, 19, 22]

	rainT = numpy.add(rainc_i, rainnc_i)

	rain_i = rainT - rainT_0

	rainT_0 = rainT

	RAIN_med = round(numpy.mean(rain_i).values.item(0),1)

	rain_t += RAIN_med

	txtfile.write("{:0>2d}-{:0>2d}-{:d},{:0>2d}:{:0>2d},{:.1f},{:.0f},{},{:.1f},{:.1f},{:.0f},{}\r\n".format(t.day, t.month, t.year, t.hour, t.minute, WS_med, WD_med, letra_med, RAIN_med, T_med, RH_med, riesgo_h))

	if t.hour == 23:
		taux = t.replace(hour=0,minute=0,second=0)
		if risk_speed >= 30 and ((taux - hoy).days > 3):
			riesgo = "Alto"
		elif risk_speed >= 20 and ((taux - hoy).days <= 3):
			riesgo = "Alto"
		elif risk_speed >= 15 and ((taux - hoy).days > 3):
			riesgo = "Moderado"
		elif risk_speed >= 10 and ((taux - hoy).days <= 3):
			riesgo = "Moderado"
		else:
			riesgo = "Bajo"

		avg_rh /= 8
		avg_rh = round(avg_rh,0)

		txt2file.write("{:0>2d}-{:0>2d}-{:d},{:.1f},{:.1f},{},{:.1f},{:.1f},{:.0f}\r\n".format(t.day, t.month, t.year, max_speed, rain_t, riesgo, max_temp, min_temp, avg_rh))

		max_speed = 0
		rain_t = 0
		risk_speed = 0
		max_temp = -273
		min_temp = 100
		avg_rh = 0

txtfile.close()
txt2file.close()
txt3file.close()

