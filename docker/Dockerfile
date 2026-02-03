# Imagen base: Python 3.11 en versión ligera
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements.txt primero (optimización de caché de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY app/ app/
COPY run.py .
COPY manage.py .

# Puerto que expone la aplicación
EXPOSE 5000

# Comando por defecto al iniciar el contenedor
CMD ["python", "run.py"]
