from django.urls import path

from .views import *

urlpatterns = [
	path('', main_page, name='index'),
	path('demand', demand, name='demand'),
	path('geography', geography, name='geography'),
	path('skills', skills, name='skills'),
	path('vacancies', vacancies, name='vacancies')

]
