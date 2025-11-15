# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo el archivo de dependencias primero (mejora cache de Docker)
COPY requirements.txt /app/

# Actualiza pip a versión segura y luego instala dependencias
RUN pip install --no-cache-dir --upgrade pip==25.3 && \
    pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la carpeta BackEnd al contenedor
COPY BackEnd /app/

# Expone el puerto en el que corre el servidor Django
EXPOSE 8000

# Asegura que las migraciones se ejecuten y crea el superusuario si es necesario
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]