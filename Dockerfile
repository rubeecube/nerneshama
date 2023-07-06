FROM tiangolo/uwsgi-nginx:python3.11

#RUN "sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout privkey.pem -out fullchain.pem -subj '/CN=nerneshama.bokobza.info'"
#sudo certbot certonly  --config-dir=certs --work-dir=certs --logs-dir=certs -d nerneshama.bokobza.info -m ruben@bokobza.info --agree-tos --no-eff-email --standalone
#sudo chown ubuntu:ubuntu certs/*

#alias launch_attached="cd ~/nerneshama/ ; sudo docker-compose down ; git pull && sudo docker-compose build --no-cache && sudo docker-compose up -e URL=nerneshama.bokobza.info"
#alias launch="launch_attached -d"

COPY app /app/

COPY certs/live/nerneshama.bokobza.info/fullchain.pem /etc/ssl/certs/cert.pem
COPY certs/live/nerneshama.bokobza.info/privkey.pem /etc/ssl/private/privkey.pem

WORKDIR /app

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/app

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]
