# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo el archivo de dependencias primero (mejora cache de Docker)
COPY requirements.txt /app/

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del backend al contenedor
COPY . /app

# Expone el puerto en el que corre el servidor Django
EXPOSE 8000

# Comando para iniciar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]