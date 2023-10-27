from fastapi import FastAPI, HTTPException, Form, Request
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


json_file_path = "data/comprar.json"
json_file_user = "data/usuarios.json"


def cargar_datos():
    try:
        with open(json_file_path, 'r') as json_file:
            return json.load(json_file) #citas
    except FileNotFoundError:
        return []


def cargar_datos_user():
    try:
        with open(json_file_user, 'r') as json_file:
            return json.load(json_file) #usuarios
    except FileNotFoundError:
        return []


def guardar_datos(data):
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file) #citas


def guardar_datos_user(data):
    with open(json_file_user, 'w') as json_file:
        json.dump(data, json_file) #usuarios


@app.post('/register')
async def register_users(request: Request,id: int = Form(...),name: str = Form(...), ape: str = Form(...),email: str = Form(...)):
    user_data = cargar_datos_user()
    user = next((item for item in user_data if item.get("id") == id), None)
    if user:
        return templates.TemplateResponse("comprar.html", {"request": request, "error": "Usuario ya registrado", "success": None})

    else:
        new_user = {
            "id":id,
            "name": name,
            "ape": ape,
            "email": email,
        }
        user_data.append(new_user)
        guardar_datos_user(user_data)
    return templates.TemplateResponse("comprar.html", {"request": request, "error": None, "success": "Usuario registrado exitosamente"})

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('comprar.html', {"request": request})

if __name__ == "__main__":
    uvicorn.run('app:app')