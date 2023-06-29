FROM tiangolo/uwsgi-nginx:python3.11

COPY app /app/
WORKDIR /app

#COPY ./cert.pem /etc/ssl/certs/cert.pem
#COPY ./privkey.pem /etc/ssl/private/privkey.pem

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/app

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]
