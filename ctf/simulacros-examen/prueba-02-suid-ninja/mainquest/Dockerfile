FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y apache2 php libapache2-mod-php python3 cron sudo netcat iputils-ping findutils && \
    apt-get clean

# Configurar web vulnerable a CMDi
RUN rm /var/www/html/index.html
COPY index.php /var/www/html/index.php
RUN chown -R www-data:www-data /var/www/html

# Crear usuario para escalada lateral
RUN useradd -m -s /bin/bash hacker && echo "hacker:hacker123" | chpasswd

# Configurar Python library hijacking
RUN mkdir -p /opt/scripts && chmod 777 /opt/scripts
COPY backup.py /opt/scripts/backup.py
RUN chown hacker:hacker /opt/scripts/backup.py && chmod 755 /opt/scripts/backup.py
RUN echo "* * * * * hacker python3 /opt/scripts/backup.py" >> /etc/crontab

# Sudo configuration for vertical escalation
RUN echo "hacker ALL=(ALL) NOPASSWD: /usr/bin/find" >> /etc/sudoers

# Flags
COPY flag_root.txt /root/flag.txt
RUN chmod 600 /root/flag.txt
COPY flag_hacker.txt /home/hacker/flag.txt
RUN chown hacker:hacker /home/hacker/flag.txt && chmod 600 /home/hacker/flag.txt

# Entrypoint
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
