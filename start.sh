#!/bin/sh
supervisord -c /etc/supervisor/supervisord.conf
supervisorctl -c /etc/supervisor/supervisord.conf
supervisorctl reread && supervisorctl update
supervisorctl -c /etc/supervisor/supervisord.conf
/usr/lib/formats/bin/python /project/FormatTools/manage.py runserver 0.0.0.0:8000