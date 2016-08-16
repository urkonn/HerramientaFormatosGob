# -*- coding: utf-8 -*-
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ConverterTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_transformar_a_formatos_abiertos(self):
        """
        Como usuario principal, yo quiero
        poder transformar mis documentos
        en Excel a formatos abiertos.

        Como usuario, la herramienta deberá
        iniciar una descarga automática 
        de mi documento con el nuevo tipo de archivo.
        """
        self.browser.get('http://0.0.0.0:8000/converter/convert/')
        self.browser.save_screenshot('Historia_1/paso1.png')

        # Revisando titulo
        self.assertEqual(self.browser.title, 'Herramienta de formatos')
        button = self.browser.find_element_by_css_selector('button#boton-recomendaciones')
        self.assertEqual(button.text, u'Recomendaciones')
        
        # Verificando vetana modal
        button.click()
        self.assertIn(self.browser.find_element_by_tag_name('body').get_attribute('class'),  'modal-open')
        self.browser.find_element_by_css_selector('button.close').click()
        self.browser.save_screenshot('Historia_1/paso2.png')
        time.sleep(2)

        # Abrir cuadro de dialogo para seleccionar xls
        span = self.browser.find_element_by_css_selector('span#selecciona')
        span.click()
        self.browser.save_screenshot('Historia_1/paso3.png')
        time.sleep(8)

        div_formatos = self.browser.find_element_by_id('div_formatos')
        boton_submit = self.browser.find_element_by_id('submitButton')

        # Verificar funcionalidad en todos los formatos
        counter = 1
        for elemento in div_formatos.find_elements_by_css_selector('a.icon'):
            self.assertFalse('icon-disabled' in elemento.get_attribute('class'))
            elemento.click()
            self.assertTrue(boton_submit.is_enabled())
            self.browser.save_screenshot('Historia_1/paso4_{0}.png'.format(str(counter)))
            counter += 1

        # Verificar enviado a conversion
        boton_submit.click()
        self.assertIn('block', self.browser.find_element_by_css_selector('div.loading-document').get_attribute('style'))
        self.browser.save_screenshot('Historia_1/paso5.png')
        time.sleep(5)

        # Verificar ventana de confirmacion para descarga
        modal_ok = self.browser.find_element_by_css_selector('div.sweet-alert')
        self.assertTrue('visible' in modal_ok.get_attribute('class'))
        self.browser.save_screenshot('Historia_1/paso6.png')

        # Descarga de archivo
        modal_ok.find_element_by_css_selector('button.confirm').click()
        self.browser.save_screenshot('Historia_1/paso7.png')
        time.sleep(3)

    def test_convertir_xls_xlsx_a_formatos_abiertos_especificos(self):
        """Como usuario, quiero que la herramienta
        me permita exportar de formatos .xls y .xslx a
        .json, .txt, .html, .csv y .xml
        """
        self.browser.get('http://0.0.0.0:8000/converter/convert/')
        self.browser.save_screenshot('Historia_2/paso1.png')

        div_formatos = self.browser.find_element_by_id('div_formatos')
        boton_submit = self.browser.find_element_by_id('submitButton')

        # Se inicia proceso para transformacion de xls
        self.proceso_descarga_formatos(div_formatos, boton_submit)

        # Se inicia proceso para transformacion de xlsx
        self.proceso_descarga_formatos(div_formatos, boton_submit, paso_test=3)

    def test_visualizacion_de_progreso(self):
        """
        Como usuario, la herramienta 
        deberia mostrar el progreso de manera visual
        que lleva la transformación de los documentos
        cargados a la herramienta.
        """

        # Verificar carga de interfaz
        self.browser.get('http://0.0.0.0:8000/converter/convert/')
        self.browser.save_screenshot('Historia_3/paso1.png')

        div_formatos = self.browser.find_element_by_id('div_formatos')
        boton_submit = self.browser.find_element_by_id('submitButton')

        # Se abre filepicker para seleccionar archivo
        span = self.browser.find_element_by_css_selector('span#selecciona')
        span.click()
        time.sleep(10)
        # Verificar nombre de archivo
        self.browser.save_screenshot('Historia_3/paso2.png')

        # Seleccion de un formato
        elemento = div_formatos.find_elements_by_css_selector('a.icon')[0]
        self.assertFalse('icon-disabled' in elemento.get_attribute('class'))
        elemento.click()
        self.assertTrue(boton_submit.is_enabled())
        self.browser.save_screenshot('Historia_3/paso3.png')

        # Se envia a conversion el archivo
        boton_submit.click()
        self.assertIn('block', self.browser.find_element_by_css_selector('div.loading-document').get_attribute('style'))
        self.browser.save_screenshot('Historia_3/paso4.png')

        time.sleep(1)
        div_flotante = self.browser.find_element_by_css_selector('div.loading-document')

        # Debe visualizarse la pantalla de progreso
        self.assertIn('display: block', div_flotante.get_attribute('style'))

        # El porcentaje tiene que ser una cadena
        self.assertFalse('' == div_flotante.find_element_by_css_selector('.percent').find_element_by_tag_name('h4').text)
        # El porcentaje debe empezar en 0
        self.assertFalse('0' == div_flotante.find_element_by_css_selector('.percent').find_element_by_tag_name('h4').text)
        self.browser.save_screenshot('Historia_3/paso5.png')
            
        time.sleep(2)

    def proceso_descarga_formatos(self, div_formatos, boton_submit, paso_test=2):
         # Verificar funcionalidad en todos los formatos
        counter = 1
        for indice_formato in range(0, 5):
            # Abrir cuadro de dialogo para seleccionar xls
            span = self.browser.find_element_by_css_selector('span#selecciona')
            span.click()
            time.sleep(8)

            # Verificar activacion de icono de formato
            elemento = div_formatos.find_elements_by_css_selector('a.icon')[indice_formato]
            self.assertFalse('icon-disabled' in elemento.get_attribute('class'))
            self.browser.save_screenshot('Historia_2/paso{0}_{1}_1.png'.format(str(paso_test), str(counter)))
            elemento.click()
            #Verificar activacion de boton submit
            self.assertTrue(boton_submit.is_enabled())
            self.browser.save_screenshot('Historia_2/paso{0}_{1}_2.png'.format(str(paso_test), str(counter)))

            # Verificar enviado a conversion
            boton_submit.click()
            self.assertIn('block', self.browser.find_element_by_css_selector('div.loading-document').get_attribute('style'))
            self.browser.save_screenshot('Historia_2/paso{0}_{1}_3.png'.format(str(paso_test), str(counter)))
            time.sleep(3)

            # Verificar ventana de confirmacion para descarga
            modal_ok = self.browser.find_element_by_css_selector('div.sweet-alert')
            self.assertTrue('visible' in modal_ok.get_attribute('class'))
            self.browser.save_screenshot('Historia_2/paso{0}_{1}_4.png'.format(str(paso_test), str(counter)))
            # Descarga de archivo
            modal_ok.find_element_by_css_selector('button.confirm').click()
            time.sleep(3)
            counter += 1

if __name__ == "__main__":
    unittest.main()
