from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq
import requests
from listaPrecios import *
import pandas as pd

urls = open("listaURLMateriales.txt","r")
listaURL = urls.readlines()
urls.close()

df_insumos=pd.DataFrame()

for url in listaURL:
	insumos = listaPrecios(url)
	df_insumos=df_insumos.append(insumos, ignore_index=True)

df_insumos.to_excel('Precios_Insumos_20200428.xls')

print(df_insumos.head())

