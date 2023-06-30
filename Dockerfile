FROM tiangolo/uwsgi-nginx:python3.9

#RUN "sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout privkey.pem -out cert.pem -subj '/CN=ec2-18-209-5-51.compute-1.amazonaws.com'"

COPY app /app/
WORKDIR /app

COPY ./cert.pem /etc/ssl/certs/cert.pem
COPY ./privkey.pem /etc/ssl/private/privkey.pem

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/app

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]
