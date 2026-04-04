FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y openssh-server python3 && apt-get clean

# SSH configuration
RUN mkdir /var/run/sshd
RUN useradd -m -s /bin/bash sshuser
RUN mkdir -p /home/sshuser/.ssh

# Configurar el reto: generaremos una llave y la pondremos en un html
COPY start.sh /start.sh
RUN chmod +x /start.sh
COPY flag.txt /home/sshuser/flag.txt
RUN chown sshuser:sshuser /home/sshuser/flag.txt && chmod 600 /home/sshuser/flag.txt

CMD ["/start.sh"]
