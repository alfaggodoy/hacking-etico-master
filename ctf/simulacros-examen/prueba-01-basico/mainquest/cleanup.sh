#!/bin/bash
# Script de mantenimiento automatizado de Rafa
cd /tmp
rm -rf *.bak
echo "Mantenimiento realizado a las $(date)" > /var/log/cleanup.log
