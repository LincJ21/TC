from fastapi import FastAPI, HTTPException, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from psycopg2.extras import RealDictCursor
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

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


json_compras = "data/compras.json"

def cargar_datos():
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Cambia la consulta SQL para buscar un usuario por número de cédula y contraseña
        query = "SELECT * FROM usuarios WHERE cc = %s AND password = %s"
        cursor.execute(query)

        # Obtén el resultado
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        return user

    except Exception as e:
        print(f"Error al cargar datos desde la base de datos: {e}")
        return None

def validar_credenciales(cc, password):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Consulta SQL para buscar un usuario por cédula y contraseña
        query = "SELECT * FROM usuarios WHERE cc = %s AND password = %s"
        cursor.execute(query, (cc, password))

        # Obtener el resultado
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        return user is not None

    except Exception as e:
        print(f"Error al validar credenciales: {e}")
        return False

def guardar_usuario(cc, name, ape, cell, email, password):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Consulta SQL para insertar un nuevo usuario
        query = "INSERT INTO usuarios (cc, name, ape, cell, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (cc, name, ape, cell, email, password))
        connection.commit()

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error al registrar usuario en la base de datos: {e}")

def cargar_datos_buy():
    try:
        with open(json_compras, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []


def guardar_datos_buy(data):
    with open(json_compras, 'w') as json_file:
        json.dump(data, json_file)


@app.post('/comprarP')
async def register_users(request: Request,id: int = Form(...),
                         name: str = Form(...), 
                         ape: str = Form(...),
                         email: str = Form(...), 
                         numero_tarjeta: str = Form(...),
                         fecha_expiracion: str = Form(...),
                         codigo_seguridad: str = Form(...)):
    buy_data = cargar_datos_buy()
    buy = next((item for item in buy_data if item.get("id") == id), None)
    if buy:
        return templates.TemplateResponse("comprar.html", {"request": request, "error": "Ya usted contrato el servicio", "success": None})

    else:
        new_buy = {
            "id":id,
            "name": name,
            "ape": ape,
            "email": email,
            "numero_tarjeta": numero_tarjeta,
            "fecha_expiracion": fecha_expiracion,
            "codigo_seguridad": codigo_seguridad,
        }
        buy_data.append(new_buy)
        guardar_datos_buy(buy_data)
    return templates.TemplateResponse("comprar.html", {"request": request, "error": None, "success": "Compra registrada exitosamente"})

@app.get('/delete/{id}')
async def delete_users(request: Request,id: int):
    buy_data = cargar_datos_buy()
    buy = next((item for item in buy_data if item.get("id") == id), None)
    
    if buy:
        buy_data.remove(buy)
        guardar_datos_buy(buy_data)
        
        return templates.TemplateResponse("listacompras.html",{"request": request,"buy_data": buy_data,"success": "¡Compra cancelada!"})
    else:
        return templates.TemplateResponse("listacompras.html",{"request": request,"buy_data": buy_data,"ERROR": "¡Compra no encontrada!"})

@app.post('/login')
async def login(request: Request, cc: str = Form(...), password: str = Form(...)):
    # Verifica si las credenciales (cédula y contraseña) son válidas
    if validar_credenciales(cc, password):
        # Credenciales válidas, redirige al usuario a su cuenta
        return templates.TemplateResponse("mi_cuenta.html", {"request": request, "error": None, "success": "Bienvenido"})
    else:
        # Credenciales inválidas, muestra un mensaje de error
        return templates.TemplateResponse("inicio_sesion.html", {"request": request, "error": "Cédula o contraseña incorrecta", "success": None})



@app.post('/registrar')
async def register_users(request: Request,
                         name: str = Form(...),
                         ape: str = Form(...),
                         cc: str = Form(...),
                         cell: str = Form(...),
                         email: str = Form(...),
                         password: str = Form(...)):
    # Verifica si el usuario con las mismas credenciales ya existe en la base de datos
    if validar_credenciales(cc, password):
        return templates.TemplateResponse("inicio_sesion.html", {"request": request, "error": "Usuario ya registrado", "success": None})
    else:
        # Registra al nuevo usuario en la base de datos
        guardar_usuario(cc, name, ape, cell, email, password)
        return templates.TemplateResponse("inicio_sesion.html", {"request": request, "error": None, "success": "Usuario registrado exitosamente"})


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

@app.get("/mi_cuenta", response_class=HTMLResponse)
def mi_cuenta(request: Request):
    return templates.TemplateResponse('mi_cuenta.html', {"request": request})

@app.get("/about_Josue", response_class=HTMLResponse)
def about_Josue(request: Request):
    return templates.TemplateResponse('about_Josue.html', {"request": request})

@app.get("/about_Cesar", response_class=HTMLResponse)
def about_Josue(request: Request):
    return templates.TemplateResponse('about_Cesar.html', {"request": request})

@app.get("/about_Carlos", response_class=HTMLResponse)
def about_Josue(request: Request):
    return templates.TemplateResponse('about_Carlos.html', {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))