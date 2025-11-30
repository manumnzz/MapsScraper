from django.urls import path
from . import views

urlpatterns = [
    path("", views.buscar_negocios, name="buscar_negocios"),
    path("exportar/", views.exportar_csv, name="exportar_csv"),

]
