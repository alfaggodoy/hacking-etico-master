FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y apache2 php libapache2-mod-php cron sudo netcat vim less && \
    apt-get clean

# Configuración web - File Upload
RUN rm /var/www/html/index.html
COPY index.php /var/www/html/index.php
RUN mkdir /var/www/html/uploads && chown -R www-data:www-data /var/www/html/uploads && chmod 777 /var/www/html/uploads

# Usuario para escalada
RUN useradd -m -s /bin/bash sysadmin && echo "sysadmin:admin12345" | chpasswd

# Simular contraseña oculta en un config.php que www-data puede leer
RUN echo "<?php // DB_PASS = 'admin12345' ?>" > /var/www/html/config.php

# Sudo for vertical escalation
RUN echo "sysadmin ALL=(ALL) NOPASSWD: /usr/bin/less" >> /etc/sudoers

# Flags
COPY flag_root.txt /root/flag.txt
RUN chmod 600 /root/flag.txt
COPY flag_sysadmin.txt /home/sysadmin/flag.txt
RUN chown sysadmin:sysadmin /home/sysadmin/flag.txt && chmod 600 /home/sysadmin/flag.txt

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
