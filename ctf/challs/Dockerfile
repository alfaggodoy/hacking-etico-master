# Imagen base ligera con Python
FROM python:3.11-slim

# Instalar dependencias
RUN pip install --no-cache-dir twisted

# Directorio de trabajo
WORKDIR /app

# Copiar todo el código
COPY . .

# Exponer los 10 puertos de los retos
EXPOSE 9001 9002 9003 9004 9005 9006 9007 9008 9009 9010

# Lanzar el servidor unificado
CMD ["python", "server.py"]
