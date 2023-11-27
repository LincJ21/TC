# cancelar_servicio.py
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from utils import autenticar_administrador, clasificar
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

@router.post("/cancelar_servicio")
async def cancelar_servicio(request: Request, id_producto: int = Form(...), contraseña: str = Form(...)):
    if request.method == 'POST':
        # Procesar la información del formulario si es una solicitud POST
        form_data = await request.form()
        cedula = form_data.get('cedula')
        contraseña = form_data.get('contraseña')
        plan_referencia = form_data.get('plan_referencia')
        id_producto = form_data.get('id_producto')
        bd = form_data.get('bd')

        try:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()

            # Verificar la contraseña
            query_verificar_contraseña = f"SELECT * FROM compras WHERE cedula = '{cedula}' AND id_compra = {id_producto} AND contraseña = '{contraseña}';"
            cursor.execute(query_verificar_contraseña)
            compra = cursor.fetchone()

            if compra:
                # Actualizar el estado del producto a "Pendiente"
                query_actualizar_estado = f"UPDATE {bd} SET estado_cuenta = 'Pendiente' WHERE id_compra = {id_producto};"
                cursor.execute(query_actualizar_estado)

                # Actualizar la columna "peticion" con el mensaje de cancelación
                query_actualizar_peticion = f"UPDATE {bd} SET peticion = 'cancelación del producto' WHERE id_compra = {id_producto};"
                cursor.execute(query_actualizar_peticion)
                # Confirmar la transacción
                connection.commit()

                return templates.TemplateResponse(
                    "home.html", {"request": request, "error": None, "success": "Servicio cancelado exitosamente"}
                )
            else:
                raise HTTPException(status_code=400, detail="Contraseña incorrecta")

        except Exception as e:
            print(f"Error al cancelar el servicio: {e}")
            return templates.TemplateResponse("error_page.html", {"request": request})

        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            connection.close()

    elif request.method == 'GET':
        # Manejar la lógica si es una solicitud GET
        cedula = request.query_params.get('cedula')
        nombre_del_producto = request.query_params.get('nombre_del_producto')
        id_producto = request.query_params.get('id_producto')
        bd = request.query_params.get('bd')

        return templates.TemplateResponse(
            "cancelar_servicio.html",
            {"request": request, "cedula": cedula, "nombre_del_producto": nombre_del_producto, "id_producto": id_producto, "bd": bd, "error": None}
        )

    # Manejar otras situaciones
    return templates.TemplateResponse("home.html", {"request": request, "error": "Error desconocido", "success": None})
