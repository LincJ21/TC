from fastapi import FastAPI, HTTPException, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import json, os
from datetime import datetime

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
json_file_user = "data/usuarios.json"


def cargar_datos():
    try:
        with open(json_file_user, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []


def cargar_datos_buy():
    try:
        with open(json_compras, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []


def guardar_datos(data):
    with open(json_file_user, 'w') as json_file:
        json.dump(data, json_file)


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
    request.cc = cc
    request.password = password
    user_data = cargar_datos()
    user = next((item for item in user_data if item.get("cc") == request.cc), None)
    if user:
        if user.get("password") == request.password:
            return templates.TemplateResponse("mi_cuenta.html", {"request": request, "error": None, "success": "Bienvenido", "name": user["name"], "ape": user["ape"]})
        else:
            return templates.TemplateResponse("inicio_sesion.html", {"request": request, "error": "Contraseña incorrecta", "success": None})
    else:
        return templates.TemplateResponse("inicio_sesion.html", {"request": request, "error": "Usuario no encontrado", "success": None})

@app.post('/registrar')
async def register_users(request: Request,
                         name: str = Form(...), 
                         ape: str = Form(...),
                         cc: str = Form(...),
                         cell: str = Form(...),
                         email: str = Form(...), 
                         password: str = Form(...)):
    user_data = cargar_datos()
    data = next((item for item in user_data if item.get("cc") == cc), None)
    if data:
        return templates.TemplateResponse("inicio_sesion.html", {"request": request, "error": "Usuario ya registrado", "success": None})

    else:
        new_user = {
            "cc": cc,
            "name": name,
            "ape": ape,
            "cell": cell,
            "email": email,
            "password": password,
        }
        user_data.append(new_user)
        guardar_datos(user_data)
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))