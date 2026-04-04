FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y vsftpd apache2 php libapache2-mod-php python3 python3-pip cron sudo wget netcat && \
    apt-get clean

# Configuración de FTP (Anon allowed, upload allowed)
COPY vsftpd.conf /etc/vsftpd.conf
RUN mkdir -p /var/run/vsftpd/empty

# Configurar Apache y los permisos
RUN mkdir -p /var/www/html/uploads && \
    chown -R root:root /var/www/html && \
    chown -R ftp:ftp /var/www/html/uploads && \
    chmod 777 /var/www/html/uploads

# Limpiar index por defecto y crear uno nuestro
RUN rm /var/www/html/index.html
COPY index.php /var/www/html/index.php

# Crear usuarios vulnerables
RUN useradd -m -s /bin/bash rafa && echo "rafa:rafa123" | chpasswd
RUN echo "rafa ALL=(ALL) NOPASSWD: /usr/bin/wget" >> /etc/sudoers

# Script vulnerable de cron (lateral movement)
COPY cleanup.sh /home/rafa/cleanup.sh
RUN chown rafa:rafa /home/rafa/cleanup.sh && chmod 777 /home/rafa/cleanup.sh
RUN echo "* * * * * rafa /home/rafa/cleanup.sh" >> /etc/crontab

# WebApp vulnerable en Python LFI
COPY app.py /opt/webapp/app.py
RUN mkdir -p /opt/webapp/templates
COPY flag.txt /root/flag.txt
RUN chmod 600 /root/flag.txt

# Entrypoint script
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
