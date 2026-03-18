# Imagen base ligera con Python
FROM python:3.11-slim

# Instalar dependencias necesarias
RUN pip install --no-cache-dir twisted

# Crear directorio de trabajo
WORKDIR /app

# Copiar todo el código
COPY . .

# Exponer los puertos usados por las challenges
EXPOSE 9006 9007 9008 9009 9010

# Comando por defecto
CMD ["python", "c6-7-8-9-10.py"]
