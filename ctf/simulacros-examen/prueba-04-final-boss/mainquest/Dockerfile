FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y vsftpd apache2 php libapache2-mod-php python3 openssh-server cron sudo wget netcat vim && \
    apt-get clean

# Configuración SSH
RUN mkdir /var/run/sshd

# Usuarios (Rafa y Sysadmin)
RUN useradd -m -s /bin/bash rafa && echo "rafa:rafa" | chpasswd
RUN useradd -m -s /bin/bash sysadmin && echo "sysadmin:sysadmin" | chpasswd

# Crear llaves SSH para Rafa para que el atacante las pueda robar vía LFI
RUN mkdir -p /home/rafa/.ssh && \
    ssh-keygen -t rsa -N "" -f /home/rafa/.ssh/id_rsa && \
    cat /home/rafa/.ssh/id_rsa.pub > /home/rafa/.ssh/authorized_keys && \
    chown -R rafa:rafa /home/rafa/.ssh && \
    chmod 600 /home/rafa/.ssh/authorized_keys && \
    chmod 600 /home/rafa/.ssh/id_rsa

# Configuración de FTP para Web Shell
COPY vsftpd.conf /etc/vsftpd.conf
RUN mkdir -p /var/run/vsftpd/empty
RUN mkdir -p /var/www/html/uploads && \
    chown -R root:root /var/www/html && \
    chown -R ftp:ftp /var/www/html/uploads && \
    chmod 777 /var/www/html/uploads
RUN echo "<?php echo 'Portal Principal. Uploads solo via FTP habilitados internamente.'; ?>" > /var/www/html/index.php

# Python Web App Vulnerable a LFI (corre en 8000)
COPY app.py /opt/webapp/app.py

# Python Library Hijacking (Cron sysadmin)
RUN mkdir -p /opt/admin_scripts && chmod 777 /opt/admin_scripts
COPY health_check.py /opt/admin_scripts/health_check.py
RUN chown sysadmin:sysadmin /opt/admin_scripts/health_check.py && chmod 755 /opt/admin_scripts/health_check.py
RUN echo "* * * * * sysadmin python3 /opt/admin_scripts/health_check.py" >> /etc/crontab

# Sudo configuration for vertical escalation
RUN echo "sysadmin ALL=(ALL) NOPASSWD: /usr/bin/vim" >> /etc/sudoers

# Banderas (Flags)
COPY flag_root.txt /root/flag.txt
RUN chmod 600 /root/flag.txt
COPY flag_sys.txt /home/sysadmin/flag.txt
RUN chown sysadmin:sysadmin /home/sysadmin/flag.txt && chmod 600 /home/sysadmin/flag.txt
COPY flag_rafa.txt /home/rafa/flag.txt
RUN chown rafa:rafa /home/rafa/flag.txt && chmod 600 /home/rafa/flag.txt

# Entrypoint
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
