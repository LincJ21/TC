from fastapi import APIRouter, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
import psycopg2

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Datos de configuración de la base de datos
db_params = {
    'host': 'roundhouse.proxy.rlwy.net',
    'user': 'postgres',
    'password': '5-5*GedCCGBaDfc2E4ea2bgcEb1*bD4*',
    'database': 'railway',
    'port': 42746
}

def autenticar_administrador(codigo: str, contraseña: str):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            query = "SELECT * FROM administradores WHERE codigo = %s AND contraseña = %s"
            cursor.execute(query, (codigo, contraseña))
            administrador = cursor.fetchone()

            return administrador is not None

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al autenticar administrador: {e}")

@router.post("/administrador")
async def iniciar_sesion_administrador(request: Request, codigo: str = Form(...), contraseña: str = Form(...)):
    try:
        if autenticar_administrador(codigo, contraseña):
            return await Tabla(request)
        else:
            raise HTTPException(status_code=401, detail="Código o contraseña incorrectos")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

async def Tabla(request: Request):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            query_familia = "SELECT * FROM familiar"
            cursor.execute(query_familia)
            datos_familia = cursor.fetchall()

            query_internet = "SELECT * FROM internet"
            cursor.execute(query_internet)
            datos_internet = cursor.fetchall()

            query_entretenimiento = "SELECT * FROM entretenimiento"
            cursor.execute(query_entretenimiento)
            datos_entretenimiento = cursor.fetchall()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {e}")

    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "datos_familia": datos_familia, "datos_internet": datos_internet, "datos_entretenimiento": datos_entretenimiento}
    )
