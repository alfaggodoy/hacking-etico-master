# Imagen base ligera con Python
FROM python:3.11-slim

# Instalar dependencias necesarias
RUN pip install --no-cache-dir twisted

# Crear directorio de trabajo
WORKDIR /app

# Copiar todo el código
COPY . .

# Exponer los puertos usados por las challenges
EXPOSE 9001 9002 9003 9005

# Comando por defecto
CMD ["python", "c1-2-3-5.py"]
