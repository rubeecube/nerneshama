#! /usr/bin/env sh
set -e

/uwsgi-nginx-entrypoint.sh

if [ -f /app/nginx.conf ]; then
  cp /app/nginx.conf /etc/nginx/conf.d/nginx.conf
else
  content_server='\n'
  content_server=$content_server'server {\n'
  content_server=$content_server'    listen 80;\n'
  content_server=$content_server"    server_name '$SRV_URL';\n"
  content_server=$content_server'    return 301 https://'$SRV_URL'$request_uri;\n'

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
