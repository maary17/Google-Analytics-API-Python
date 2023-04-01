# Google-Analytics-API-Python
API Google Analytics junto Python para obtener información sobre cómo los usuarios usan un sitio web o aplicación. Ayuda a analizar y mejorar la experiencia del usuario de manera eficiente.


## Habilitar la API de Google Analytics

Para habilitar la API de Google Analytics en la consola de desarrolladores de Google, sigue estos pasos:

1. Ve a la consola de desarrolladores de Google (https://console.developers.google.com/)
2. Selecciona el proyecto en el que deseas habilitar la API de Google Analytics.
3. Haz clic en "Habilitar APIs y servicios".
4. Busca "Google Analytics API" y haz clic en ella.
5. Haz clic en "Habilitar".

## Obtener las credenciales necesarias

Para obtener las credenciales necesarias para acceder a la API de Google Analytics desde Python, sigue estos pasos:

1. Ve a la consola de Google Cloud Platform (https://console.cloud.google.com/)
2. Selecciona el proyecto en el que deseas crear las credenciales.
3. Haz clic en "Crear credenciales" y selecciona "ID de cliente de OAuth".
4. Selecciona "Aplicación de escritorio" como tipo de aplicación.
5. Agrega un nombre a la credencial y haz clic en "Crear".
6. En la pantalla de detalles de la credencial, haz clic en "Descargar" para descargar el archivo JSON que contiene las credenciales.

## Instalar bibliotecas

Por último, deberás instalar las bibliotecas `google-auth` y `google-api-python-client` en tu entorno de Python. Puedes hacerlo utilizando el siguiente comando en la línea de comandos:

# Instalar bibliotecas
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

Con estas bibliotecas instaladas, estarás listo para comenzar a trabajar con la API de Google Analytics desde Python.
