# -*- coding: utf-8 -*-
import os
import time
from django.test import TestCase, Client
from .converters import save_temporary_xls, limpia_nombre_archivo, XLSConverter, XLSToCSVConverter, XLSToJSONConverter, XLSToTxtConverter, XLSToXMLConverter, XLSToHTMLConverter
from django.conf import settings


xls_test = u'Excel Prueba para conversión 80KB.xls'
xlsx_test = u'Excel prueba conversión 70KB.xlsx'
xls_path_externo = os.path.join(settings.TEMPORAL_FILES_ROOT, 'xls/test/')


# Create your tests here.
class ConverterIOTest(TestCase):
    def setUp(self):
        self.xls_path = xls_path_externo

        self.xls_file_name = xls_test
        self.xlsx_file_name = xlsx_test

        self.testing_xls = open(os.path.join(self.xls_path, self.xls_file_name))
        self.testing_xlsx = open(os.path.join(self.xls_path, self.xlsx_file_name))

    def test_save_temporal_file(self):
        """
        Los archivos que se van a convertir
        deben quedar guardados en el path
        para xls, xlsx temporales
        ../media/files/xls/
        """
        self.assertEqual(save_temporary_xls(self.testing_xls), u'{0}xls/Excel Prueba para conversión 80KB.xls'.format(settings.TEMPORAL_FILES_ROOT))
        self.assertEqual(save_temporary_xls(self.testing_xlsx), u'{0}xls/Excel prueba conversión 70KB.xlsx'.format(settings.TEMPORAL_FILES_ROOT))

    def test_obtener_nombre_archivo_limpio(self):
        """
        Al manejar un archivo debe ser capaz
        de obtener solo el nombre del archivo
        sin la ruta
        """
        self.assertEqual(limpia_nombre_archivo(self.testing_xls.name), self.xls_file_name)
        self.assertEqual(limpia_nombre_archivo(self.testing_xlsx.name), self.xlsx_file_name)

    def test_tipo_de_convertidor_por_formato(self):
        """
        Al manejar un archivo debe ser capaz
        de distingo correctamente el tipo de manejador
        para la conversion. De lo contrario debe mandar nulo
        """
        formatos_permitidos = [('csv', XLSToCSVConverter), ('json', XLSToJSONConverter), ('txt', XLSToTxtConverter), ('xml', XLSToXMLConverter), ('html', XLSToHTMLConverter)]
        formatos_no_permitidos = ['pdf', 'odt', 'ai']

        for formato_permitido in formatos_permitidos:
            self.assertIsInstance(XLSConverter.get_converter(formato_permitido[0], u'{0}xls/Excel Prueba para conversión 80KB.xls'.format(settings.TEMPORAL_FILES_ROOT), xls_name=self.xls_file_name), formato_permitido[1])

        for format_no_permitido in formatos_no_permitidos:
            self.assertEqual(XLSConverter.get_converter(format_no_permitido, u'{0}xls/Excel Prueba para conversión 80KB.xls'.format(settings.TEMPORAL_FILES_ROOT), xls_name=self.xls_file_name), None)


class ConverterHTTPTest(TestCase):
    def setUp(self):
        self.xls_path = xls_path_externo

        self.xls_file_name = xls_test
        self.xlsx_file_name = xlsx_test

        self.testing_xls = open(os.path.join(self.xls_path, self.xls_file_name))
        self.testing_xlsx = open(os.path.join(self.xls_path, self.xlsx_file_name))

        self.dowload_xls = ''
        self.dowload_xlsx = ''

        self.cliente = Client()

    def test_upload_xls_a_csv(self):
        """
        Debe ser capaz de subir un archivo xls
        con un HTTP Post para transformarlo a CSV
        y recobrar un json como respuesta 
        con el estatus ok y una URL de seguimiento
        """
        respuesta = self.cliente.post('/converter/convert/', {'xls_file': self.testing_xls, 'format_to': 'csv'})
        self.assertEqual(respuesta.json()['status'], 'ok')
        self.assertIn('/converter/progress/', respuesta.json()['link'])

    def test_upload_xls_a_json(self):
        """
        Debe ser capaz de subir un archivo xls
        con un HTTP Post para transformarlo a JSON
        y recobrar un json como respuesta 
        con el estatus ok y una URL de seguimiento
        """
        respuesta = self.cliente.post('/converter/convert/', {'xls_file': self.testing_xls, 'format_to': 'json'})
        self.assertEqual(respuesta.json()['status'], 'ok')
        self.assertIn('/converter/progress/', respuesta.json()['link'])

    def test_upload_xls_a_html(self):
        """
        Debe ser capaz de subir un archivo xls
        con un HTTP Post para transformarlo a HTML
        y recobrar un json como respuesta 
        con el estatus ok y una URL de seguimiento
        """
        respuesta = self.cliente.post('/converter/convert/', {'xls_file': self.testing_xls, 'format_to': 'html'})
        self.assertEqual(respuesta.json()['status'], 'ok')
        self.assertIn('/converter/progress/', respuesta.json()['link'])

    def test_upload_xls_a_txt(self):
        """
        Debe ser capaz de subir un archivo xls
        con un HTTP Post para transformarlo a TXT
        y recobrar un json como respuesta 
        con el estatus ok y una URL de seguimiento
        """
        respuesta = self.cliente.post('/converter/convert/', {'xls_file': self.testing_xls, 'format_to': 'txt'})
        self.assertEqual(respuesta.json()['status'], 'ok')
        self.assertIn('/converter/progress/', respuesta.json()['link'])

    def test_upload_xls_a_xml(self):
        """
        Debe ser capaz de subir un archivo xls
        con un HTTP Post para transformarlo a XML
        y recobrar un json como respuesta 
        con el estatus ok y una URL de seguimiento
        """
        respuesta = self.cliente.post('/converter/convert/', {'xls_file': self.testing_xls, 'format_to': 'xml'})
        self.assertEqual(respuesta.json()['status'], 'ok')
        self.assertIn('/converter/progress/', respuesta.json()['link'])

    def test_upload_xlsx_a_csv(self):
        """
        Debe ser capaz de subir un archivo xlsx
        con un HTTP Post para transformarlo a CSV
        y recobrar un json como respuesta 
        con el estatus ok y una URL de seguimiento
        """
        respuesta = self.cliente.post('/converter/convert/', {'xls_file': self.testing_xlsx, 'format_to': 'csv'})
        self.assertEqual(respuesta.json()['status'], 'ok')
        self.assertIn('/converter/progress/', respuesta.json()['link'])

    def test_upload_xlsx_a_json(self):
        """
        Debe ser capaz de subir un archivo xlsx
        con un HTTP Post para transformarlo a JSON
        y recobrar un json como respuesta 
        con el estatus ok y una URL de seguimiento
        """
        respuesta = self.cliente.post('/converter/convert/', {'xls_file': self.testing_xlsx, 'format_to': 'json'})
        self.assertEqual(respuesta.json()['status'], 'ok')
        self.assertIn('/converter/progress/', respuesta.json()['link'])

    def test_upload_xlsx_a_html(self):
        """
        Debe ser capaz de subir un archivo xlsx
        con un HTTP Post para transformarlo a HTML
        y recobrar un json como respuesta 
        con el estatus ok y una URL de seguimiento
        """
        respuesta = self.cliente.post('/converter/convert/', {'xls_file': self.testing_xlsx, 'format_to': 'html'})
        self.assertEqual(respuesta.json()['status'], 'ok')
        self.assertIn('/converter/progress/', respuesta.json()['link'])

    def test_upload_xlsx_a_txt(self):
        """
        Debe ser capaz de subir un archivo xlsx
        con un HTTP Post para transformarlo a TXT
        y recobrar un json como respuesta 
        con el estatus ok y una URL de seguimiento
        """
        respuesta = self.cliente.post('/converter/convert/', {'xls_file': self.testing_xlsx, 'format_to': 'txt'})
        self.assertEqual(respuesta.json()['status'], 'ok')
        self.assertIn('/converter/progress/', respuesta.json()['link'])

    def test_upload_xlsx_a_xml(self):
        """
        Debe ser capaz de subir un archivo xlsx
        con un HTTP Post para transformarlo a XML
        y recobrar un json como respuesta 
        con el estatus ok y una URL de seguimiento
        """
        respuesta = self.cliente.post('/converter/convert/', {'xls_file': self.testing_xlsx, 'format_to': 'xml'})
        self.assertEqual(respuesta.json()['status'], 'ok')
        self.assertIn('/converter/progress/', respuesta.json()['link'])

    def test_download_xls_file(self):
        """
        Debe ser capaz de descargar los archivos
        xls que se han mandado a convertir previamente
        Se consideran los formatos: csv, json, html, txt, xml
        """
        for formato in ['csv', 'json', 'html', 'txt', 'xml']:
            # Esperamos a que termine el background job
            time.sleep(5)
            respuesta = self.cliente.get(u'/converter/download/{0}/{1}'.format(formato, xls_test.replace('xls', formato)))

            self.assertEqual(respuesta.status_code, 200)

    def test_download_xlsx_file(self):
        """
        Debe ser capaz de descargar los archivos
        xlsx que se han mandado a convertir previamente
        Se consideran los formatos: csv, json, html, txt, xml
        """
        for formato in ['csv', 'json', 'html', 'txt', 'xml']:
            # Esperamos a que termine el background job
            time.sleep(5)
            respuesta = self.cliente.get(u'/converter/download/{0}/{1}'.format(formato, self.xlsx_file_name.replace('xlsx', formato)))
            self.assertEqual(respuesta.status_code, 200)
