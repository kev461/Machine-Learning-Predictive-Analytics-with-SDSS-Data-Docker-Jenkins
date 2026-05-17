# Imagen base
FROM python:3.10

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar todo el proyecto
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto Flask
EXPOSE 5000

# Ejecutar la aplicación
CMD ["python", "run.py"]