from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^convert/$', views.convert_to, name='convert_to'),
	url(r'^(?P<path>[-_a-zA-Z0-9]+)/(?P<file_name>.*)', views.download_file, name='download_file'),
]