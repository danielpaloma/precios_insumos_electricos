from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq
import requests
import pandas as pd
import numpy as np

def listaPrecios(url):
	def isBlank (myString):
	    if myString and myString.strip():
	        #myString is not None AND myString is not empty or blank
	        return False
	    #myString is None OR myString is empty or blank
	    return True

	my_url = url
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll("td",{"class":"info"})
	k=len(containers)
	i=0
	nombre_cable=[0 for _ in range(k)]
	precios_cables=[0 for _ in range(k)]
	precio_final=[0 for _ in range(k)]

	#1. Extraer los nombres de insumos y sus precios

	for i in range(k):
		try:
			nombre_cable[i] = containers[i].td.a.b.get_text()
		except AttributeError:
			nombre_cable[i]=""

		try:
			precios_cables[i] = containers[i].find("td",{"width":"160"}).get_text()
		except AttributeError:
			precios_cables[i]=""
		except isBlank(precios_cables[i]):
			precios_cables[i]=""

		i+=1

	#1.1 dando formato al precio
	for i in range(k):
		if isBlank(precios_cables[i])!=True:
			p_a = precios_cables[i].split()
			p_b = p_a[1].split("P")
			precio_final[i] = p_b[0].replace(",","")
			precio_final[i]=int(precio_final[i])
		else:
			pass

	#2. creando un Dataframe cuyas columnas son: nombre, precio
	df = pd.DataFrame(list(zip(nombre_cable, precio_final)), 
               columns =['Nombre_insumo', 'Precio_($)']) 

	#2.1 eliminar las filas que tengan "nombre_insumo" en blanco:

	df['Nombre_insumo'].replace('',np.nan, inplace=True)
	df.dropna(subset=['Nombre_insumo'],inplace=True)

	return df
