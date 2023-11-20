# nuevo_contrato.py
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from utils import clasificar
import psycopg2
router = APIRouter()
templates = Jinja2Templates(directory="templates")

db_params = {
    'host': 'roundhouse.proxy.rlwy.net',
    'user': 'postgres',
    'password': '5-5*GedCCGBaDfc2E4ea2bgcEb1*bD4*',
    'database': 'railway',
    'port': 42746
}

@router.route("/nuevo_contrato", methods=['GET', 'POST'])
async def nuevo_contrato(request: Request):
    if request.method == 'POST':
        form_data = await request.form()
        cedula = form_data.get('cedula')
        contraseña = form_data.get('contraseña')
        plan_referencia = form_data.get('plan_referencia')
        try:
            
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            # Verificar la contraseña
            query_verificar_contraseña = f"SELECT * FROM compras WHERE cedula = '{cedula}'  AND contraseña = '{contraseña}';"
            cursor.execute(query_verificar_contraseña)
            compra = cursor.fetchone()

            if compra:
                # Llama a tu función clasificar
                clasificar(cedula, plan_referencia)
                # Si todo va bien, puedes retornar una respuesta exitosa o redirigir a otra página
                return templates.TemplateResponse("listacompras.html", {"request": request})
            else:
                raise HTTPException(status_code=400, detail="Contraseña incorrecta")

        except Exception as e:
            # Manejar las excepciones según tus necesidades
            return templates.TemplateResponse("error.html", {"request": request, "error_message": str(e)})
    elif request.method == 'GET':
        plan_referencial = request.query_params.get('plan_referencia')
        return templates.TemplateResponse(
            "nuevo_contrato.html",
            {"request": request, "plan_referencia": plan_referencial, "error": None}
        )

    # Manejar otras situaciones
    return templates.TemplateResponse("home.html", {"request": request, "error": "Error desconocido", "success": None})
