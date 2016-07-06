# HerramientaFormatosGob
Herramienta para convertir formatos XLS, XLSX a formatos abiertos. Esta herramienta esta construida en la ultima versión de Django (1.9.7). 

Requermimientos
===============
°Python 2.7
°.. _Virtualenv: https://virtualenv.pypa.io/en/stable/


Instalación Local
=================
Los siguientes pasos asumen que se han instalado los requerimientos señalados anteriormente::

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








