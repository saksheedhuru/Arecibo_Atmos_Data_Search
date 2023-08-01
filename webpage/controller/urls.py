from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('gallery', views.gallery, name = 'gallery'),
    path('interferometer_calendar', views.interferometer_calendar, name = 'interferometer_calendar'),
    path('interferometer_files', views.interferometer_files, name = 'interferometer_files')

]