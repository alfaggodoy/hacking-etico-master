#!/bin/bash
# Generate SSH key and expose the private key via a basic python HTTP server
ssh-keygen -t rsa -N "" -f /tmp/id_rsa
cat /tmp/id_rsa.pub > /home/sshuser/.ssh/authorized_keys
chown -R sshuser:sshuser /home/sshuser/.ssh
chmod 600 /home/sshuser/.ssh/authorized_keys
chmod 700 /home/sshuser/.ssh

# Start SSH
/usr/sbin/sshd

# Expose private key via HTTP
mkdir -p /opt/web
mv /tmp/id_rsa /opt/web/id_rsa
cd /opt/web
python3 -m http.server 8080
