FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3 netcat socat && apt-get clean
COPY jail.py /jail.py
COPY flag.txt /flag.txt
RUN chmod +x /jail.py
CMD socat TCP-LISTEN:9000,reuseaddr,fork EXEC:"python3 /jail.py"
