FROM ubuntu:20.04
RUN apt-get update && apt-get install -y netcat socat bash && apt-get clean
COPY challenge.sh /challenge.sh
COPY flag.txt /flag.txt
RUN chmod +x /challenge.sh
CMD socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"/challenge.sh"
