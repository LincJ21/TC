from fastapi import FastAPI, HTTPException, Form, Request, Response, Depends, Header, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import os
import psycopg2
import jwt

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Nuevos datos de configuración
db_params = {
    'host': 'roundhouse.proxy.rlwy.net',
    'user': 'postgres',
    'password': '5-5*GedCCGBaDfc2E4ea2bgcEb1*bD4*',
    'database': 'railway',
    'port': 42746
}

SECRET_KEY = "tu_clave_secreta"
ALGORITHM = "HS256"

def create_session_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def read_session_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def cargar_datos(cc):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        query = "SELECT cc, nombre, apellido, telefono, correo FROM usuarios WHERE cc = %s"
        cursor.execute(query, (cc,))

        user = cursor.fetchone()

        if user:
            user_cc, user_name, user_ape, user_cell, user_email = user
        else:
            user_cc, user_name, user_ape, user_cell, user_email = None, None, None, None, None

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error al realizar la consulta: {e}")
        user_cc, user_name, user_ape, user_cell, user_email = None, None, None, None, None

    return user_cc, user_name, user_ape, user_cell, user_email

def validar_credenciales(cc, password):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        query = "SELECT * FROM usuarios WHERE cc = %s AND contraseña = %s"
        cursor.execute(query, (cc, password))

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        return user is not None

    except Exception as e:
        print(f"Error al validar credenciales: {e}")
        return False


def guardar_usuario(cc, name, ape, cell, email, password, direction):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        query = "INSERT INTO usuarios (cc, nombre, apellido,  correo, contraseña, telefono, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (cc, name, ape,  email, password, cell, direction))
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
async def register_users(request: Request, id: int = Form(...),
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
            "id": id,
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
async def delete_users(request: Request, id: int):
    buy_data = cargar_datos_buy()
    buy = next((item for item in buy_data if item.get("id") == id), None)

    if buy:
        buy_data.remove(buy)
        guardar_datos_buy(buy_data)

        return templates.TemplateResponse("listacompras.html",
                                          {"request": request, "buy_data": buy_data, "success": "¡Compra cancelada!"})
    else:
        return templates.TemplateResponse("listacompras.html",
                                          {"request": request, "buy_data": buy_data, "ERROR": "¡Compra no encontrada!"})


@app.post('/login')
async def login(request: Request, cc: str = Form(...), password: str = Form(...)):
    if validar_credenciales(cc, password):
        session_token = create_session_token({"sub": cc})
        user_data = cargar_datos(cc)  # Obtener información del usuario
        response = templates.TemplateResponse(
            "mi_cuenta.html",
            {"request": request, "user_data": user_data, "error": None, "success": None}
        )
        response.set_cookie(key="session_token", value=session_token)
        return response
    else:
        raise HTTPException(status_code=401, detail="Cédula o contraseña incorrecta")

# Ruta para cerrar sesión y eliminar la cookie
@app.post('/logout')
async def logout(response: Response, request: Request):
    response.delete_cookie(key="session_token")
    return templates.TemplateResponse(
            "home.html",
            {"request": request, "user_data": None, "error": None, "success": None}
        )


# Ruta para la página 'mi_cuenta'
@app.get('/mi_cuenta')
async def mi_cuenta(request: Request, session_token: str = Cookie(None)):
    if session_token is None:
        return render_template('mi_cuenta.html', request, user_data=None, error="No hay sesión iniciada", success=None)

    try:
        payload = read_session_token(session_token)
        cc = payload.get("sub")
        user_data = cargar_datos(cc)
        return render_template('mi_cuenta.html', request, user_data=user_data, error=None, success=None)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token de sesión expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token de sesión no válido")



@app.post('/registrar')
async def register_users(name: str = Form(...),
                         ape: str = Form(...),
                         cc: str = Form(...),
                         cell: str = Form(...),
                         email: str = Form(...),
                         password: str = Form(...),
                         direction: str = Form(...)):
    # Verifica si el usuario con las mismas credenciales ya existe en la base de datos
    if validar_credenciales(cc, password):
        return {"error": "Usuario ya registrado", "success": None}
    else:
        # Registra al nuevo usuario en la base de datos, incluyendo los campos de tarjeta de crédito
        guardar_usuario(cc, name, ape, cell, email, password, direction)
        return {"error": None, "success": "Usuario registrado exitosamente"}

def render_template(template_name: str, request: Request, user_data: dict = None, error: str = None, success: str = None):
    return templates.TemplateResponse(template_name, {"request": request, "user_data": user_data, "error": error, "success": success})


# Función genérica para renderizar páginas con autenticación
def render_authenticated_page(template_name: str, request: Request, session_token: str = Cookie(None)):
    if session_token is None:
        return render_template(template_name, request, user_data=None, error="No hay sesión iniciada", success=None)

    try:
        payload = read_session_token(session_token)
        cc = payload.get("sub")
        user_data = cargar_datos(cc)
        return render_template(template_name, request, user_data=user_data, error=None, success=None)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token de sesión expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token de sesión no válido")

# Rutas utilizando la función genérica
@app.get("/", response_class=HTMLResponse)
def render_home_page(request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('home.html', request, session_token)

@app.get("/{page}", response_class=HTMLResponse)
def render_authenticated_page_by_name(page: str, request: Request, session_token: str = Cookie(None)):
    # Usar el nombre de la página para construir el nombre del template
    template_name = f"{page}.html"
    return render_authenticated_page(template_name, request, session_token)

# Rutas utilizando la función genérica
@app.get("/{about}", response_class=HTMLResponse)
def render_about_page(about: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('about.html', request, session_token)

@app.get("/{listacompras}", response_class=HTMLResponse)
def render_listacompras_page(listacompras: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('listacompras.html', request, session_token)

@app.get("/{servicios}", response_class=HTMLResponse)
def render_servicios_page(servicios: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('servicios.html', request, session_token)

@app.get("/{comprar}", response_class=HTMLResponse)
def render_comprar_page(comprar: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('comprar.html', request, session_token)

@app.get("/{inicio_sesion}", response_class=HTMLResponse)
def render_inicio_sesion_page(inicio_sesion: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('inicio_sesion.html', request, session_token)

@app.get("/{registro_usuario}", response_class=HTMLResponse)
def render_registro_usuario_page(registro_usuario: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('registro_usuario.html', request, session_token)

@app.get("/{about_Carlos}", response_class=HTMLResponse)
def render_registro_usuario_page(about_Carlos: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('about_Carlos.html', request, session_token)

@app.get("/{about_Cesar}", response_class=HTMLResponse)
def render_registro_usuario_page(about_Cesar: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('about_Cesar.html', request, session_token)

@app.get("/{about_Josue}", response_class=HTMLResponse)
def render_registro_usuario_page(about_Josue: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('about_Josue.html', request, session_token)

@app.get("/{help}", response_class=HTMLResponse)
def render_registro_usuario_page(help: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('help.html', request, session_token)

@app.get("/{cobertura}", response_class=HTMLResponse)
def render_registro_usuario_page(cobertura: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('cobertura.html', request, session_token)

@app.get("/{entretenimiento}", response_class=HTMLResponse)
def render_registro_usuario_page(entretenimiento: str, request: Request, session_token: str = Cookie(None)):
    return render_authenticated_page('entretenimiento.html', request, session_token)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", 8000)))
