from django.urls import path
from . import views

app_name = "myapp"

urlpatterns = [
    # Home / Landing
    path("", views.home, name="home"),

    # Formulario
    path("save-formulario/", views.save_formulario, name="save_formulario"),

    # Landings de servicios odontopediátricos
    path("servicios/prevencion/", views.prevencion_controles, name="servicio_prevencion"),
    path("servicios/primera-consulta-bebe/", views.primera_consulta_bebe, name="servicio_bebe"),
    path("servicios/restauradores/", views.tratamientos_restauradores, name="servicio_restauradores"),
    path("servicios/odontologia-sin-miedo/", views.odontologia_sin_miedo, name="servicio_sin_miedo"),
    path("servicios/educacion-habitos/", views.educacion_habitos, name="servicio_educacion"),


    # Legales
    path("politicas-privacidad/", views.politicas_privacidad, name="politicas_privacidad"),
]
