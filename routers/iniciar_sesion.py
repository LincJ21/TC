# iniciar_sesion.py
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from utils import autenticar_administrador

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.route('/iniciar_sesion', methods=['GET', 'POST'])
async def iniciar_sesion(request: Request):
    if request.method == 'POST':
        # Procesar la información del formulario si es una solicitud POST
        form_data = await request.form()
        id_producto = form_data.get('id_producto')
        nombre_del_producto = form_data.get('nombre_del_producto')
        cedula = form_data.get('cedula')
        bd = form_data.get('bd')
        if not id_producto or not nombre_del_producto:
            return templates.TemplateResponse(
                "listacompras.html",
                {"request": request, "error": "Error al procesar la cancelación"}
            )
        else:
            return templates.TemplateResponse(
                "inicio_sesion.html", {"request": request, "id_producto": id_producto, "nombre_del_producto": nombre_del_producto,"cedula":cedula, "bd":bd, "error": None})

    elif request.method == 'GET':
        
        # Manejar la lógica si es una solicitud GET
        id_producto = request.query_params.get('id_producto')
        nombre_del_producto = request.query_params.get('nombre_del_producto')
        cedula=request.query_params.get('cedula')
        bd = request.query_params.get('bd')
        return templates.TemplateResponse("inicio_sesion.html", {"request": request, "id_producto": id_producto, "nombre_del_producto": nombre_del_producto,"cedula":cedula, "bd":bd, "error": None})

    # Manejar otras situaciones
    return templates.TemplateResponse("listacompras.html", {"request": request, "error": "Error desconocido"})
