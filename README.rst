HerramientaFormatosGob
======================
Herramienta para convertir formatos XLS, XLSX a formatos abiertos. Esta herramienta esta construida en la ultima versión de Django (1.9.7). 

Requermimientos
===============
- `Python 2.7`__.
- Virtualenv_
- Redis_

.. _Virtualenv: https://virtualenv.pypa.io/en/stable/
.. _Redis: http://redis.io/
.. _Python27: https://www.python.org/download/releases/2.7/
.. _Docker: https://www.docker.com/products/overview
__ Python27_


Instalación Local
=================
Los siguientes pasos asumen que se han instalado los requerimientos señalados anteriormente. Correr los siguientes comandos::

  git clone git@github.com:vaquer/HerramientaFormatosGob.git
  virtualenv {{TU_VIRTUALENV}}
  . {{TU_VIRTUALENV}}/bin/activate
  pip install -r HerramientaFormatosGob/requirements.txt

Uso Local
=========
Para poder ver la herramienta corra el siguiente comando::

   python HerramientaFormatosGob/FormatTools/manage.py runserver

Despues en el navegador::

http://127.0.0.1:8000/converter/convert

Instalación Docker
=================
Para los siguientes pasos se require tener instalada la plataforma Docker_ en el servidor aplicativo.

En el servidor aplicativo construimos la imagen del contenedor::

  git clone git@github.com:vaquer/HerramientaFormatosGob.git
  docker build -t {{nombre_de_imagen}} HerramientaFormatosGob/.

Una vez construida la imagen Docker de la herramienta, ya es posible generar el contenedor donde estara ejecutandose la herramienta. Un punto a considerar antes de avanzar con la creación del contenedor es que el contenedor necesita un volumen para poder trabajar, el volumen debera apuntar a la ruta interna /project/FormatTools/media del contenedor.

Otro aspecto a considerar es que la herramienta hace uso de la tecnologia Redis como background en el manejo de colas (para guardar el estado y la comunicación con los procesos), por lo que se necesita crear contenedores Docker de Redis y los conectarlos al contenedor aplicativo.

Los comandos de consola para correr la aplicacion con toda la arquitectura necesaria son los siguientes::

  docker run --name redistask -p 6379:6379 -d redis
  docker run --name redisresp -p 6378:6379 -d redis
  docker run --name formats -v {{ruta_del_host_para_volumen}}:/project/FormatTools/media -e SECRET_KEY="{{secret_key}}" --link redistask:redistask --link redisresp:redisresp -e FQDN="http://tudominio.com/" -e DEBUG=False -p 80:80 formats


Despues en el navegador::

http://tudominio.com/converter/convert