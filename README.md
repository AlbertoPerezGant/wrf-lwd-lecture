# Programa de analisis de direccion de viento de ficheros WRF

Los ficheros wrf son ficheros que contienen una gran cantidad de datos de previsiones meterorológicas, los cuales pueden ocupar varios GB de información. Es por ello que extraer dichos datos, limpiarlos y analizarlos debidamente es esencial para poder realizar una correcta previsión. 

En este repositorio se muestra un script para poder obtener histogramas de la dirección del viento en diferentes horas del día. Estos histogramas son individuales por lo que aparecerá unicamente una dirección pero es posible modificar el programa para poder obtener histogramas de diferentes tramos horarios.

En primer lugar debemos contar con un directorio llamado **/wrf** que es de donde el script obtendrá la información relativa al archivo wrf. Dentro de este directorio hay una serie de directorios con el nombre **/DD-MM-YYY** el cual tendremos que escribir en terminal. Una vez hecho esto podremos visualizar el resultado del analisis.

El script wrf.py está pensado para que se pueda analizar la información extraida de un archivo wrf con el siguiente formato **wrfout_d03_YYYY-MM-DD_hh_mm_ss**, lo cual genera una serie de archivos txt que se guardarán en la carpeta mencionada en el anterior párrafo.

En este repositorio no he puesto ningún archivo wrf ya que los que dispongo ocupan mucho espacio, pero debería de funcionar dando como resultado una serie de histogramas comparativos.
