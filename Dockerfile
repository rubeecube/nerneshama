FROM tiangolo/uwsgi-nginx:python3.11

#RUN "sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout privkey.pem -out fullchain.pem -subj '/CN=nerneshama.bokobza.info'"

#alias launch_attached="cd ~/nerneshama/ ; sudo docker-compose down ; git pull && sudo docker-compose build --no-cache && sudo docker-compose up"
#alias launch="launch_attached -d"

COPY app /app/
WORKDIR /app

COPY *certs/live/nerneshama.bokobza.info-0001/fullchain.pem /etc/ssl/certs/cert.pem
COPY *certs/live/nerneshama.bokobza.info-0001/privkey.pem /etc/ssl/private/privkey.pem

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/app

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]
