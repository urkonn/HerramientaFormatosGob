FROM ubuntu:14.04
MAINTAINER Francisco Vaquero <francisco@opi.la>

ENV FORMAT_HOME /usr/lib/formats

RUN mkdir /project && \
	mkdir -p /usr/lib/formats /var/log/celery/

RUN apt-get update && \
	apt-get install -y supervisor python-virtualenv git && \
    virtualenv $FORMAT_HOME

RUN git clone https://github.com/vaquer/HerramientaFormatosGob.git /project && \
    $FORMAT_HOME/bin/pip install -r /project/requirements.txt
    
COPY format_celery.conf /etc/supervisor/conf.d/format_celery.conf
COPY format_celerybeat.conf /etc/supervisor/conf.d/format_celerybeat.conf
COPY supervisord.conf /etc/supervisor/supervisord.conf

RUN touch /var/log/celery/format_beat.log && touch /var/log/celery/format_worker.log

EXPOSE 8000

ADD start.sh /start.sh

ENTRYPOINT ["/start.sh"]

