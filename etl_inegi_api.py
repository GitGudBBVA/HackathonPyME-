import pandas as pd
import requests
import json
from Levenshtein import ratio
from decouple import config

TOKEN_INEGI = config('TOKEN_INEGI')
df = pd.read_csv('HackatonBBVA/Final_Data_Hackathon_2022.csv')

def normalize2(s):
    replacements = (
        ("SA DE CV", ""),
        (",",""),
        (".","") ,
        ("SA CV","")
    )
    for a,b in replacements:
        s = s.replace(a,b)
    return s

business_company = []
name = []
activity = []
stratum = []
web_site = []
longitude = []
latitude = []

for i in range(df.shape[0]):
    company = df['NombComp'].iloc[i]
    business_company.append(company)
    company = normalize2(company).strip()
    res = requests.get(f'https://www.inegi.org.mx/app/api/denue/v1/consulta/Nombre/{company}/00/1/5/{TOKEN_INEGI}')
    data = res.json()

    if res.status_code == 200:
        for i in range(len(data)):
            np = data[i]['Razon_social']
            coincidence = ratio(company,np)

            if coincidence > 0.85:
                name.append(data[i]['Nombre'])
                activity.append(data[i]['Clase_actividad'])
                stratum.append(data[i]['Estrato'])
                web_site.append(data[i]['Sitio_internet'])
                longitude.append(data[i]['Longitud'])
                latitude.append(data[i]['Latitud'])
            else:
                name.append('sin dato')
                activity.append('sin dato')
                stratum.append('sin dato')
                web_site.append('sin dato')
                longitude.append('sin dato')
                latitude.append('sin dato')
                break
    else:
        name.append('sin dato')
        activity.append('sin dato')
        stratum.append('sin dato')
        web_site.append('sin dato')
        longitude.append('sin dato')
        latitude.append('sin dato')

diccionario = {
    'business_company':business_company,
    'name':name,
    'activity':activity,
    'stratum':stratum,
    'web_site':web_site,
    'longitude':longitude,
    'latitude':latitude
}

dato_diccionario = pd.DataFrame(diccionario)
data_unida = pd.concat([df,dato_diccionario])