from fastapi import FastAPI, HTTPException, Form, Request, Response,Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import json, os
import psycopg2
# Nuevos datos de configuración
db_params = {
    'host': 'roundhouse.proxy.rlwy.net',
    'user': 'postgres',
    'password': '5-5*GedCCGBaDfc2E4ea2bgcEb1*bD4*',
    'database': 'railway',
    'port': 42746
}
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def compra_ya_registrada(cedula):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Consulta SQL para verificar si existe una compra para la cédula dada
        query = "SELECT * FROM compras WHERE cedula = %s"
        cursor.execute(query, (cedula,))
        existing_compra = cursor.fetchone()

        cursor.close()
        connection.close()

        return existing_compra is not None
    except Exception as e:
        print(f"Error al verificar si la compra ya está registrada: {e}")
        return False


def cargar_datos(cc):
    try:
        # Establecer la conexión a la base de datos usando los parámetros
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        # Cambia la consulta SQL para buscar un usuario por número de cédula
        query = "SELECT cc, nombre, apellido, telefono, correo FROM usuarios WHERE cc = %s"
        cursor.execute(query, (cc,))
        user = cursor.fetchone()
        if user:
            user_cc, user_name, user_ape, user_cell, user_email = user
        else:
            user_cc, user_name, user_ape, user_cell, user_email = None, None, None, None, None
        cursor.close()
        connection.close()
        # Imprime los valores antes de retornarlos
        print("user_cc:", user_cc)
        print("user_name:", user_name)
        print("user_ape:", user_ape)
        print("user_cell:", user_cell)
        print("user_email:", user_email)
    except Exception as e:
        print(f"Error al realizar la consulta: {e}")
        user_cc, user_name, user_ape, user_cell, user_email = None, None, None, None, None
    return user_cc, user_name, user_ape, user_cell, user_email


def guardar_compra(cedula, nombre, apellido, correo, departamento, ciudad_pueblo, barrio, celular, numero_tarjeta, fecha_expiracion, codigo_seguridad):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        # Consulta SQL para insertar una nueva compra
        query = """
            INSERT INTO compras (
                cedula, nombre, apellido, correo, departamento, ciudad_pueblo,
                barrio, celular, numero_tarjeta, fecha_expiracion, codigo_seguridad
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            cedula, nombre, apellido, correo, departamento, ciudad_pueblo,
            barrio, celular, numero_tarjeta, fecha_expiracion, codigo_seguridad
        ))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error al registrar compra en la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor al procesar la compra")

@app.post('/comprarP')
async def register_users(request: Request, cc: str = Form(...),
                         nombre: str = Form(...),
                         apellido: str = Form(...),
                         email: str = Form(...),
                         departamento: str = Form(...),
                         ciudad_pueblo: str = Form(...),
                         barrio: str = Form(...),
                         celular: str = Form(...),
                         numero_tarjeta: str = Form(...),
                         fecha_expiracion: str = Form(...),
                         codigo_seguridad: str = Form(...)):
    # Verificar si la compra ya ha sido registrada
    if compra_ya_registrada(cc):
        return templates.TemplateResponse("comprar.html", {"request": request, "error": "Ya usted contrato el servicio", "success": None})
    else:
        # Registrar la compra en la base de datos
        guardar_compra(cc, nombre, apellido, email, departamento, ciudad_pueblo, barrio, celular, numero_tarjeta, fecha_expiracion, codigo_seguridad)
        return templates.TemplateResponse("comprar.html", {"request": request, "error": None, "success": "Compra registrada exitosamente"})


@app.get('/delete/{id}')
async def delete_users(request: Request, id_compra: int):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Consulta SQL para eliminar la compra por ID
        query = "DELETE FROM compras WHERE id_compra = %s"
        cursor.execute(query, (id_compra,))

        connection.commit()
        cursor.close()
        connection.close()

        return templates.TemplateResponse("listacompras.html", {"request": request, "success": "¡Compra cancelada!"})
    except Exception as e:
        print(f"Error al cancelar la compra en la base de datos: {e}")
        return templates.TemplateResponse("listacompras.html", {"request": request, "ERROR": "Error al cancelar la compra"})


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})
@app.get("/listacompras", response_class=HTMLResponse)
def index(request: Request):
    buy_data=cargar_datos_buy()
    return templates.TemplateResponse('listacompras.html', {"request": request, "buy_data": buy_data})
@app.get("/about", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('about.html', {"request": request})
@app.get("/servicios", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('servicios.html', {"request": request})
@app.get("/comprar", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('comprar.html', {"request": request})
@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})
@app.get("/inicio_sesion", response_class=HTMLResponse)
def inicio_sesion(request: Request):
    return templates.TemplateResponse('inicio_sesion.html', {"request": request})
@app.get("/registro_usuario", response_class=HTMLResponse)
def registrar_usuario(request: Request):
    return templates.TemplateResponse('registro_usuario.html', {"request": request})
@app.get("/entretenimiento", response_class=HTMLResponse)
def entretenimiento(request: Request):
    return templates.TemplateResponse('entretenimiento.html', {"request": request})
@app.get("/about_Josue", response_class=HTMLResponse)
def about_Josue(request: Request):
    return templates.TemplateResponse('about_Josue.html', {"request": request})
@app.get("/about_Cesar", response_class=HTMLResponse)
def about_Josue(request: Request):
    return templates.TemplateResponse('about_Cesar.html', {"request": request})
@app.get("/about_Carlos", response_class=HTMLResponse)
def about_Josue(request: Request):
    return templates.TemplateResponse('about_Carlos.html', {"request": request})
@app.get("/help", response_class=HTMLResponse)
def help(request: Request):
    return templates.TemplateResponse('help.html', {"request": request})
@app.get("/internet", response_class=HTMLResponse)
def internet(request: Request):
    return templates.TemplateResponse('internet.html', {"request": request})
@app.get("/cobertura", response_class=HTMLResponse)
def cobertura(request: Request):
    return templates.TemplateResponse('cobertura.html', {"request": request})
@app.get("/familiar", response_class=HTMLResponse)
def familiar(request: Request):
    return templates.TemplateResponse('familiar.html', {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))