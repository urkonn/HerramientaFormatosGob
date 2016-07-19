from __future__ import absolute_import
from celery.decorators import task
from django.conf import settings
from .converters import XLSConverter


@task(bind=True, name="Transformacion de XLS")
def transform_file(self, file_path, format_to, xls_name):
    """
    Task Celery que se encarga del proceso
    de transformacion de los xls y xlsx
    """
    #try:
    converter_engine = XLSConverter.get_converter(format_to.encode('utf-8'), file_path.encode('utf-8'), xls_name.encode('utf-8'))
    #except Exception, file_error:
    #    raise Exception(file_error)

    # Inicio de proceso de conversion
    for progress in converter_engine.convert():
        # Se actualiza el estado de la tarea
        self.update_state(state='PROGRESS',meta={'current': progress})
    # Finalmente se retorna el link de descarga
    return converter_engine.get_download_link()

    def on_failure(self, *args, **kwargs):
        pass