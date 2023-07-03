FROM tiangolo/uwsgi-nginx:python3.11

#RUN "sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout privkey.pem -out cert.pem -subj '/CN=ec2-18-209-5-51.compute-1.amazonaws.com'"

#alias launch="cd ~/nerneshama/ ; sudo docker-compose down ; git pull && sudo docker-compose build --no-cache && sudo docker-compose up -d"
#alias launch_attached="cd ~/ner_neshama/ ; sudo docker stop ner_neshama ; sudo docker rm ner_neshama ; git pull && sudo docker build -t ner_neshama . && sudo docker run -d -p 80:80 -p 443:443 --name ner_neshama -v ~/ner_neshama/db:/app/db ner_neshama"

COPY app /app/
WORKDIR /app

COPY ../certs/live/nerneshama.bokobza.info/fullchain.pemcert.pem /etc/ssl/certs/cert.pem
COPY ../certs/live/nerneshama.bokobza.info/privkey.pem /etc/ssl/private/privkey.pem

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/app

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]
