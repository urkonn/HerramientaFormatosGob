import os
from celery.result import AsyncResult
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, Http404, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from .converters import XLSConverter, save_temporary_xls
from .tasks import transform_file


# Create your views here.
def convert_to(request):
    """ 
    Vista que procesa la conversion 
    de un archivo XLS, XLSX a un formato destino
    URL: /converter/convert/
    Tipo Respuesta: JSON
    """
    # Se regresa el Formulario si no es peticion POST
    if request.method != 'POST':
        return render(request, 'convert.html', {'settings': settings})

    # Se validan los parametros POST
    xls_file = request.FILES.get('xls_file', None)
    format_to = request.POST.get('format_to', None)

    if not xls_file or not format_to:
        raise Http404

    # Guardado temporal del xls o xlsx
    xls_file_path = save_temporary_xls(xls_file)

    # Creacion de la celery task
    result_celery = transform_file.delay(xls_file_path, format_to, xls_file.name)
    
    try:
        return JsonResponse({'status': 'ok', 'link': '{0}converter/progress/{1}/'.format(settings.FQDN, result_celery.task_id)})
    except Exception, convert_error:
        return JsonResponse({'status': 'error', 'error': '{0}'.format(convert_error)})


def download_file(request, path, file_name):
    """ 
    Vista que procesa la descarga de un archivo temporal
    URL: /converter/download/{format}/{filename}
    Tipo Respuesta: HTTP RESPONSE Streaming
    """

    xls_base = os.path.join(settings.TEMPORAL_FILES_ROOT, 'xls/')

    # Se recupera el archivo temporal
    try:
        path_base = os.path.join(settings.TEMPORAL_FILES_ROOT, path)
        temp_path = os.path.join(path_base, file_name)
        file = open(temp_path.encode('utf-8'))
    except IOError, e:
       raise Http404

    # Se genera la respuesta HTTP para la descarga
    response = StreamingHttpResponse((line for line in file), content_type='{0}'.format(XLSConverter.get_mime_type_of_file(path)))
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_name.encode('utf-8'))
    
    # Se elimina el archivo temporal del disco duro
    try:
        os.remove(temp_path.encode('utf-8'))
    except:
        pass

    # Se eliminan los archivos xls temporales
    try:
        xls_path = os.path.join(xls_base, file_name.replace(path, 'xls'))
        os.remove(xls_path.encode('utf-8'))
    except:
        try:
            xls_path = os.path.join(xls_base, file_name.replace(path, 'xlsx'))
            os.remove(xls_path.encode('utf-8'))
        except:
            pass

    return response


@csrf_exempt
def get_progress_task(request, task_id):
    """
    Vista que retorna el % de progreso de una tarea
    URL: /converter/progress/{task_id}/
    Respuesta: JsonResponse
    """
    #if request.method != 'POST':
    #    raise Http404

    result = AsyncResult(task_id)
    
    if result.ready():
        try:
            return JsonResponse({'link': result.result, 'status': result.status})
        except Exception, e:
            return JsonResponse({'status': 'ERROR', 'progress': str(e)})

    if result.status == 'PROGRESS':
        try:
            return JsonResponse({'status': result.status, 'progress': result.result})
        except Exception, e:
            return JsonResponse({'status': 'ERROR', 'error': str(e)})

    return JsonResponse({'status': 'ERROR', 'error': 'Lo sentimos vuelve a intentarlo mas tarde', 'status': result.status})

