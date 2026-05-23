from django.urls import path

from . import views

app_name = "myapp"

urlpatterns = [
    path("", views.home, name="home"),
    path("save-formulario/", views.save_formulario, name="save_formulario"),
    path("servicios/odontologia-general/", views.odontologia_general, name="servicio_odontologia_general"),
    path("servicios/implantologia/", views.implantologia, name="servicio_implantologia"),
    path("servicios/odontopediatria/", views.odontopediatria, name="servicio_odontopediatria"),
    path("politicas-privacidad/", views.politicas_privacidad, name="politicas_privacidad"),
]
