FROM debian:bullseye

RUN apt-get update && apt-get install -y \
    tor \
    python3 \
    python3-pip && \
    pip3 install flask requests

# Copy your app
COPY tor_mirror.py /app/tor_mirror.py
WORKDIR /app

# Hidden service dir setup with correct permissions
RUN mkdir -p /var/lib/tor/hidden_service && \
    chmod 700 /var/lib/tor/hidden_service

# Copy torrc config file
COPY torrc /etc/tor/torrc

EXPOSE 8080

CMD tor & python3 tor_mirror.py
