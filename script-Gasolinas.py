#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from datetime import timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# In[2]:


def send_mail(destinatario_ : list):
    
    print("Enviando email")
    
    # Iniciamos los parámetros del script
    remitente = 'actinverdc@gmail.com'
    asunto = 'Información de gasolinas diarias'
    cuerpo = ''
    ruta_adjunto = 'InfoGas.csv'
    nombre_adjunto = 'InfoGas.csv'

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()

    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatario_)
    mensaje['Subject'] = asunto

    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_adjunto, 'rb')

    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)

    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)

    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login('actinverdc@gmail.com','Actinver2021**')

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatario_, texto)

    # Cerramos la conexión
    sesion_smtp.quit()
    
    print("SE ENVIO EL CORREO EXITOSAMENTE")


# In[3]:


def get_date():
    '''
    Return the current day and month
    '''
    today = datetime.today() #-  timedelta(days=1)
    return today.strftime('%d-%b')


def retieve_data():
    '''
    Retrieve Data about oil in this page 'https://petrointelligence.com/precios-de-la-gasolina-y-diesel-hoy.php'
    '''
    
    url = "https://petrointelligence.com/precios-de-la-gasolina-y-diesel-hoy.php"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    b = soup.find_all('b')

    precios = []
    for i in range(0,len(b)):
        if '$/litro' in b[i].text:
            precios.append(b[i+1].text)
    
    row_nacional = []
    row_cdmx = []
    row_jalisco = []
    row_NL = []
    row_nacional.extend([get_date(), 'Nacional', precios[0], precios[1], precios[2], precios[4]])
    row_cdmx.extend([get_date(), 'CDMX', precios[6], precios[7], precios[8], 'N/A'])
    row_jalisco.extend([get_date(), 'Jalisco', precios[9], precios[10], precios[11], 'N/A'])
    row_NL.extend([get_date(), 'Nuevo León', precios[12], precios[13], precios[14], 'N/A'])
    data = [row_nacional,row_cdmx,row_jalisco,row_NL]
    
    print("Se realizo correctamente la extraccion de datos")
    
    return pd.DataFrame(data)


# In[5]:


def main():
    '''
    Main funtion
    '''
    ####Get data
    df = retieve_data()
    
    ####Save Data
    df.to_csv('InfoGas.csv', index=False, header=False, mode='a')
    
    ####Send Data
    send_mail(['314159735@pcpuma.acatlan.unam.mx'])
    #send_mail(['314159735@pcpuma.acatlan.unam.mx','agaliciad@actinver.com.mx'])


# In[6]:


main()


# In[ ]:




