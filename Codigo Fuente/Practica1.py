# Practica 1. Tipología y ciclo de vida de los datos
"""
Created on Mon Nov  5 21:52:41 2018

@author: Nacho
"""

import os
import requests
import csv
from bs4 import BeautifulSoup

def variacion(s_url,fecha_inicio,fecha_fin,tbl_variacionIPC):
    response = requests.post(s_url)
    #response = requests.post("http://www.ine.es/varipc/verVariaciones.do?idmesini=1&anyoini=2010&idmesfin=9&anyofin=2018&ntipo=2&enviar=Calcular")
    soup = BeautifulSoup(response.text,"html.parser")
    table = soup.find("table")
    for row in table.findAll("tr"):
        cells = row.findAll('td')
        if len(cells)==2:
            comunidad = str(cells[0].get_text())
            variacion = str(cells[1].get_text())
            comunidad = comunidad.replace("\r","")
            comunidad = comunidad.replace("\t","")
            comunidad = comunidad.replace("\n","")
            comunidad = comunidad.strip(" ")
            variacion = variacion.replace("\r","")
            variacion = variacion.replace("\t","")
            variacion = variacion.replace("\n","")
            variacion = variacion.strip(" ")
            segmento = [fecha_inicio,fecha_fin,comunidad,variacion]
            tbl_variacionIPC.append(segmento)
    return

tbl_variacionIPC = []
Nom_columnas = [ "Fecha_Inicio","Fecha_Fin","Comunidad","Variacion"]
tbl_variacionIPC.append(Nom_columnas)

mes_inicio = 1
anio_inicio = 2010
mes_fin = mes_inicio + 1
anio_fin = 2010
url = "http://www.ine.es/varipc/verVariaciones.do?"
param_calcular = "&ntipo=2&enviar=Calcular"


while mes_fin < 10 or anio_fin <= 2011:
    param_mini = "&idmesini=" + str(mes_inicio)
    param_aini = "&anyoini=" +  str(anio_inicio)
    param_mfin = "&idmesfin=" + str(mes_fin)
    param_afin = "&anyofin=" + str(anio_fin)
    s_url = url + param_mini + param_aini + param_mfin + param_afin + param_calcular
    fecha_inicio = str(mes_inicio) + str(anio_inicio)
    fecha_fin = str(mes_fin) +  str(anio_fin)
        
    variacion (s_url,fecha_inicio,fecha_fin,tbl_variacionIPC)
#    print(str(mes_inicio) + "M" + str(anio_inicio) + "A\n" + str(mes_fin)  + "M" + str(anio_fin) + "A\n")
    
    mes_inicio = mes_inicio +1
    mes_fin = mes_fin + 1
    if (mes_inicio - 12) == 1:
        anio_inicio =  anio_inicio +1
        mes_inicio = mes_inicio -12
        
    if mes_fin - 12 == 1:
        anio_fin = anio_fin + 1 
        mes_fin = mes_fin - 12 
    
currentdir = os.path.dirname(__file__)
nom_fichero = "Variacion_IPC.csv"
path = os.path.join(currentdir,nom_fichero)

with open(path,"w", newline ='') as csvfile:
    writer = csv.writer(csvfile,delimiter=',')
    for row in tbl_variacionIPC:
        writer.writerow(row)
    