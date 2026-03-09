# Este archivo es un script de shell que se utiliza para automatizar el proceso de construcción y despliegue de una aplicación Django. A continuación, se describen los pasos que realiza este script:

#!/usr/bin/env bash
# exit on error
set -o errexit

# poetry install
pip install -r requirements.txt # Este comando instala todas las dependencias necesarias para ejecutar la aplicación, que se encuentran listadas en el archivo requirements.txt. Es importante asegurarse de que este archivo esté actualizado con todas las dependencias necesarias para evitar problemas de ejecución.

python manage.py collectstatic --noinput
python manage.py migrate

# Tenemos que ejecutar el comando chmod a+x build.sh para darle permisos de ejecución al script, lo que es necesario para poder ejecutarlo desde la terminal. Este comando se debe ejecutar una sola vez después de crear el script, y luego se podrá ejecutar el script con ./build.sh cada vez que se necesite construir y desplegar la aplicación.

# pip install gunicorn uvicorn y pip freeze > requirements.txt para generar el archivo de requisitos que se utilizará en producción. Gunicorn es un servidor WSGI para aplicaciones Python, y Uvicorn es un servidor ASGI para aplicaciones asíncronas. Ambos son opciones populares para servir aplicaciones Django en producción, dependiendo de si la aplicación es síncrona o asíncrona. El comando pip freeze > requirements.txt se utiliza para generar un archivo de requisitos que incluye todas las dependencias necesarias para ejecutar la aplicación en producción, lo que facilita la instalación de estas dependencias en el entorno de producción.