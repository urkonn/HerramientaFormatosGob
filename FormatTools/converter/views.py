import os
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, Http404, StreamingHttpResponse
from .converters import XLSConverter


# Create your views here.
def convert_to(request):
    """ Vista que procesa la conversion 
    de un archivo XLS, XLSX a un formato destino
    URL: /converter/convert/
    Tipo Respuesta: JSON
    """
    # Se regresa el Formulario si no es peticion POST
    if request.method != 'POST':
        return render(request, 'convert.html')

    # Se validan los parametros POST
    xls_file = request.FILES.get('xls_file', None)
    format_to = request.POST.get('format_to', None)

    if not xls_file or not format_to:
        raise Http404

    # Se obtiene el objeto para convertir el archivo dependiendo del formato
    try:
        converter_engine = XLSConverter.get_converter(format_to, xls_file)
    except Exception, file_error:
        return JsonResponse({'status': 'error', 'error': '{0}'.format(file_error)})

    if not converter_engine:
        raise Http404

    try:
        return JsonResponse({'status': 'ok', 'link': converter_engine.convert()})
    except Exception, convert_error:
        return JsonResponse({'status': 'error', 'error': '{0}'.format(convert_error)})


def download_file(request, path, file_name):
    """ Vista que procesa la descarga de un archivo temporal
    URL: /converter/(format)/(filename)
    Tipo Respuesta: HTTP RESPONSE Streaming
    """

    xls_base = os.path.join(settings.TEMPORAL_FILES_ROOT, 'xls/')
    # Se recupera el archivo temporal
    try:
        path_base = os.path.join(settings.TEMPORAL_FILES_ROOT, path)
        file = open(os.path.join(path_base, file_name))
    except IOError, e:
        raise Http404

    # Se genera la respuesta HTTP para la descarga
    response = StreamingHttpResponse((line for line in file), content_type='{0}'.format(XLSConverter.get_mime_type_of_file(path)))
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_name.encode('utf-8'))
    
    # Se elimina el archivo temporal del disco duro
    os.remove(os.path.join(path_base, file_name))
    try:
        os.remove(os.path.join(xls_base, file_name.replace(path, 'xls')))
    except:
        os.remove(os.path.join(xls_base, file_name.replace(path, 'xlsx')))

    return response
