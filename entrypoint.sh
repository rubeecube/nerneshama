#! /usr/bin/env sh
set -e

/uwsgi-nginx-entrypoint.sh

if [ -f /app/nginx.conf ]; then
  cp /app/nginx.conf /etc/nginx/conf.d/nginx.conf
else
  content_server='\n'
  content_server=$content_server'server {\n'
  content_server=$content_server'    listen 80;\n'
  content_server=$content_server"    server_name ec2-18-209-5-51.compute-1.amazonaws.com;\n"
  content_server=$content_server'    return 301 https://nerneshama.bokobza.info$request_uri;\n'
  content_server=$content_server'}\n'

  content_server=$content_server'server {\n'
  content_server=$content_server"    listen 443 ssl default_server;\n"
  content_server=$content_server"    server_name nerneshama.bokobza.info;\n"
  content_server=$content_server"    ssl_protocols    TLSv1.2;\n"
  content_server=$content_server"    ssl_ciphers AES256+EECDH:AES256+EDH:!aNULL;\n"
  content_server=$content_server"    ssl_prefer_server_ciphers    on;\n"
  content_server=$content_server"    add_header   Strict-Transport-Security   \"max-age=31536000; includeSubDomains; preload\"  always;\n"
  content_server=$content_server"    ssl_session_cache    shared:SSL:10m;\n"
  content_server=$content_server"    ssl_session_timeout  10m;\n"
  content_server=$content_server"    ssl_certificate  /etc/ssl/certs/cert.pem;\n"
  content_server=$content_server"    ssl_certificate_key  /etc/ssl/private/privkey.pem;\n"

  content_server=$content_server'    location / {\n'
  content_server=$content_server'        proxy_set_header Host $host;\n'
  content_server=$content_server'        proxy_pass http://127.0.0.1:5000;\n'
  content_server=$content_server'        proxy_redirect off;\n'
  content_server=$content_server'    }\n'

  content_server=$content_server'}\n'

  printf "$content_server" >/etc/nginx/conf.d/nginx.conf
fi

# For Alpine:
# Explicitly add installed Python packages and uWSGI Python packages to PYTHONPATH
# Otherwise uWSGI can't import Flask
if [ -n "$ALPINEPYTHON" ]; then
  export PYTHONPATH=$PYTHONPATH:/usr/local/lib/$ALPINEPYTHON/site-packages:/usr/lib/$ALPINEPYTHON/site-packages
fi

exec "$@"
