FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3 netcat socat && apt-get clean
COPY challenge.py /challenge.py
COPY flag.txt /flag.txt
RUN chmod +x /challenge.py
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 /challenge.py"
