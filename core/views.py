from __future__ import annotations

from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Formulario


WHATSAPP_NUMBER = "5491170621055"
DIRECCION_LOCAL = "Besares 2477, 3°D, Nuñez, Capital Federal"

SERVICIOS = [
    {
        "key": "odontopediatria",
        "nombre": "Odontopediatría",
        "url_name": "servicio_odontopediatria",
    },
    {
        "key": "odontologia_general",
        "nombre": "Odontología general",
        "url_name": "servicio_odontologia_general",
    },
    {
        "key": "implantologia",
        "nombre": "Implantología y rehabilitación oral",
        "url_name": "servicio_implantologia",
    },
]


def _base_context(**extra):
    ctx = {
        "servicios_menu": SERVICIOS,
        "telefono_whatsapp": WHATSAPP_NUMBER,
        "direccion_local": DIRECCION_LOCAL,
        "site_name": "Aura Odontologia",
    }
    ctx.update(extra)
    return ctx


def detectar_origen(request) -> str:
    if request.GET.get("gclid"):
        return "google_ads"
    if request.GET.get("fbclid"):
        return "facebook_ads"

    utm_source = (request.GET.get("utm_source") or "").lower().strip()
    if utm_source in {"google", "googleads", "adwords"}:
        return "google_ads"
    if utm_source in {"facebook", "instagram", "meta"}:
        return "facebook_ads"
    if utm_source in {"whatsapp"}:
        return "whatsapp"
    if utm_source in {"organico", "organic", "seo"}:
        return "organico"

    return "directo"


def _sanitize_choice(value: str, allowed: set[str], default: str) -> str:
    v = (value or "").strip()
    return v if v in allowed else default


def send_user_data_email(user_data: str) -> None:
    subject = "Nuevo formulario web"
    body = f"Se registró un nuevo formulario con los siguientes datos:\n\n{user_data}"

    from_email = "notificaciondepaginaweb@gmail.com"
    to = ["notificaciondepaginaweb@gmail.com"]
    bcc = [
        "maximobatallan@gmail.com",
        "od.alessandrello@gmail.com",
    ]

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to,
        bcc=bcc,
    )
    email.send(fail_silently=False)


def home(request):
    formulario_enviado = bool(request.GET.get("ok"))
    origen = detectar_origen(request)

    ctx = _base_context(
        is_home=True,
        formulario_enviado=formulario_enviado,
        page_title="Aura Odontologia | Odontología integral para todas las edades",
        page_description=(
            "Odontología integral para todas las edades. Especialistas en odontopediatría, "
            "odontología general e implantología y rehabilitación oral. Atención profesional, "
            "cercana y personalizada con turnos por WhatsApp."
        ),
        whatsapp_text="Hola, quiero sacar un turno. ¿Me pasan disponibilidad?",
        producto="general",
        origen=origen,
    )
    return render(request, "myapp/pages/home.html", ctx)


@require_POST
def save_formulario(request):
    nombre = (request.POST.get("name") or "").strip()
    telefono = (request.POST.get("telefono") or "").strip()
    email = (request.POST.get("email") or "").strip()
    texto = (request.POST.get("message") or "").strip()

    servicios_validos = {k for (k, _) in Formulario.SERVICIOS_CHOICES}
    origenes_validos = {k for (k, _) in Formulario.ORIGEN_CHOICES}

    producto = _sanitize_choice(request.POST.get("producto"), servicios_validos, "general")
    origen = _sanitize_choice(request.POST.get("origen"), origenes_validos, "directo")

    gclid = (request.POST.get("gclid") or "").strip()
    fbclid = (request.POST.get("fbclid") or "").strip()

    utm_source = (request.POST.get("utm_source") or "").strip()
    utm_medium = (request.POST.get("utm_medium") or "").strip()
    utm_campaign = (request.POST.get("utm_campaign") or "").strip()
    utm_term = (request.POST.get("utm_term") or "").strip()
    utm_content = (request.POST.get("utm_content") or "").strip()

    next_url = (request.POST.get("next") or "").strip()
    landing_path = next_url or request.path

    Formulario.objects.create(
        nombre=nombre,
        telefono=telefono,
        mail=email,
        texto=texto,
        producto=producto,
        origen=origen,
        gclid=gclid,
        fbclid=fbclid,
        utm_source=utm_source,
        utm_medium=utm_medium,
        utm_campaign=utm_campaign,
        utm_term=utm_term,
        utm_content=utm_content,
        landing_path=landing_path,
    )

    user_data = (
        f"nombre: {nombre}\n"
        f"telefono: {telefono}\n"
        f"email: {email}\n"
        f"producto: {producto}\n"
        f"texto: {texto}"
    )
    send_user_data_email(user_data)

    if next_url:
        sep = "&" if "?" in next_url else "?"
        return redirect(f"{next_url}{sep}ok=1")

    return redirect(f"{reverse('myapp:home')}?ok=1")


def politicas_privacidad(request):
    ctx = _base_context(
        is_home=False,
        page_title="Políticas de Privacidad | Aura Odontologia",
        page_description="Políticas de privacidad de Aura Odontologia.",
    )
    return render(request, "myapp/politicas_privacidad.html", ctx)


def odontopediatria(request):
    origen = detectar_origen(request)
    ctx = _base_context(
        is_home=False,
        active_producto="odontopediatria",
        page_title="Odontopediatría | Aura Odontologia",
        page_description=(
            "Atención especializada para bebés, niños y adolescentes en un entorno cálido y de "
            "confianza, con foco en hábitos saludables y controles periódicos."
        ),
        producto="odontopediatria",
        origen=origen,
        whatsapp_text="Hola, quiero sacar un turno para odontopediatría.",
    )
    return render(request, "myapp/servicios/odontopediatria.html", ctx)


def odontologia_general(request):
    origen = detectar_origen(request)
    ctx = _base_context(
        is_home=False,
        active_producto="odontologia_general",
        page_title="Odontología general | Aura Odontologia",
        page_description=(
            "Odontología general para todas las edades con controles, limpiezas, restauraciones "
            "estéticas, urgencias y tratamientos integrales para cada caso."
        ),
        producto="odontologia_general",
        origen=origen,
        whatsapp_text="Hola, quiero consultar por odontología general.",
    )
    return render(request, "myapp/servicios/odontologia_general.html", ctx)


def implantologia(request):
    origen = detectar_origen(request)
    ctx = _base_context(
        is_home=False,
        active_producto="implantologia",
        page_title="Implantología y rehabilitación oral | Aura Odontologia",
        page_description=(
            "Implantología y rehabilitación oral para recuperar función, estética y comodidad "
            "con tratamientos personalizados."
        ),
        producto="implantologia",
        origen=origen,
        whatsapp_text="Hola, quiero consultar por implantología y rehabilitación oral.",
    )
    return render(request, "myapp/servicios/implantologia.html", ctx)
