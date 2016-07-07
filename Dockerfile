FROM python:2.7-alpine
MAINTAINER Julio Acuña <urkonn@gmail.com>

RUN mkdir /project

RUN apk add --no-cache git

RUN git clone https://github.com/vaquer/HerramientaFormatosGob.git /project && \
    pip install -r /project/requirements.txt

EXPOSE 8000
CMD ["python", "project/FormatTools/manage.py", "runserver", "0.0.0.0:8000"]

