# Usa la imagen oficial de Python 3.8 en Alpine
FROM python:3.11.2

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo requirements.txt e instala las dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos al contenedor
COPY . .

# Define variables de entorno para la conexión a la base de datos
ENV DB_HOST=localhost
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword
ENV DB_NAME=mydatabase
ENV DB_PORT=port

# Configura variables de entorno si es necesario
# ENV DJANGO_SETTINGS_MODULE=myproject.settings

# Usa un entrypoint para ejecutar migraciones y luego iniciar el servidor de desarrollo
ENTRYPOINT ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
