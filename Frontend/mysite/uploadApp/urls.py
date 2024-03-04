from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index , name='index'),
	url(r'^base', views.base , name='base'),
	url(r'^success$', views.success , name='success'),
	url(r'test',views.test, name='test'),
	url(r'^removeFile', views.removeFile , name='removeFile')

]