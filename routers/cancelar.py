# routers/cancelar.py
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from fastapi import HTTPException, Request
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

@router.get("/cancelar1", response_class=HTMLResponse)
async def cancelar(request: Request, id_familiar: int = Query(...)):
    try:
        cancelar_producto1(id_familiar)
        return templates.TemplateResponse("inicio_sesion_admin.html", {"request": request})

    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": f"Error: {e}"})

@router.get("/activar1", response_class=HTMLResponse)
async def activar(request: Request, id_familiar: int = Query(...)):
    try:
        activar_producto1(id_familiar)
        return templates.TemplateResponse("inicio_sesion_admin.html", {"request": request})

    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": f"Error: {e}"})

@router.get("/cancelar2", response_class=HTMLResponse)
async def cancelar(request: Request, id_familiar: int = Query(...)):
    try:
        cancelar_producto2(id_familiar)
        return templates.TemplateResponse("inicio_sesion_admin.html", {"request": request})

    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": f"Error: {e}"})

@router.get("/activar2", response_class=HTMLResponse)
async def activar(request: Request, id_familiar: int = Query(...)):
    try:
        activar_producto2(id_familiar)
        return templates.TemplateResponse("inicio_sesion_admin.html", {"request": request})

    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": f"Error: {e}"})

@router.get("/cancelar3", response_class=HTMLResponse)
async def cancelar(request: Request, id_familiar: int = Query(...)):
    try:
        cancelar_producto3(id_familiar)
        return templates.TemplateResponse("inicio_sesion_admin.html", {"request": request})

    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": f"Error: {e}"})

@router.get("/activar3", response_class=HTMLResponse)
async def activar(request: Request, id_familiar: int = Query(...)):
    try:
        activar_producto3(id_familiar)
        return templates.TemplateResponse("inicio_sesion_admin.html", {"request": request})

    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": f"Error: {e}"})

def cancelar_producto1(id_familiar: int):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            query = f"UPDATE familiar SET estado_cuenta = 'Cancelado', peticion = NULL WHERE id_familiar = {id_familiar};"
            cursor.execute(query)
            connection.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cancelar el producto: {e}")

def activar_producto1(id_familiar: int):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            query = f"UPDATE familiar SET estado_cuenta = 'Activo', peticion = NULL WHERE id_familiar = {id_familiar};"
            cursor.execute(query)
            connection.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al activar el producto: {e}")
    
def cancelar_producto2(id_familiar: int):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            query = f"UPDATE internet SET estado_cuenta = 'Cancelado', peticion = NULL WHERE id_internet = {id_familiar};"
            cursor.execute(query)
            connection.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cancelar el producto: {e}")

def activar_producto2(id_familiar: int):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            query = f"UPDATE internet SET estado_cuenta = 'Activo', peticion = NULL WHERE id_interent = {id_familiar};"
            cursor.execute(query)
            connection.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al activar el producto: {e}")

def cancelar_producto3(id_familiar: int):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            query = f"UPDATE entretenimiento SET estado_cuenta = 'Cancelado', peticion = NULL WHERE id_entretenimiento = {id_familiar};"
            cursor.execute(query)
            connection.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cancelar el producto: {e}")

def activar_producto3(id_familiar: int):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            query = f"UPDATE entretenimiento SET estado_cuenta = 'Activo', peticion = NULL WHERE id_entretenimiento = {id_familiar};"
            cursor.execute(query)
            connection.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al activar el producto: {e}")
