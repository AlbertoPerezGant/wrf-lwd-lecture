# Programa de analisis de direccion de viento de ficheros WRF

Los ficheros wrf son ficheros que contienen una gran cantidad de datos de previsiones meterorológicas, los cuales pueden ocupar varios GB de información. Es por ello que extraer dichos datos, limpiarlos y analizarlos debidamente es esencial para poder realizar una correcta previsión. 

En este repositorio se muestra un script para poder obtener histogramas de la dirección del viento en diferentes horas del día. Estos histogramas son individuales por lo que aparecerá unicamente una dirección pero es posible modificar el programa para poder obtener histogramas de diferentes tramos horarios.

En primer lugar debemos contar con un directorio llamado **/wrf** que es de donde el script obtendrá la información relativa al archivo wrf. Este script está pensado para que el usuario pueda introducir desde su terminal el día del que quiere extraer la información a partir de un archivo con el formato **wrfout_d03_YYYY-MM-DD_hh_mm_ss** por lo que preguntará por terminal en que día desea realizar el analisis de entre una lista de posibles respuestas.

