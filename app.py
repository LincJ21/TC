from fastapi import FastAPI, HTTPException, Form, Request, Response,Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import date, timedelta# main.py
from routers import admin, consulta, cancelar, cancelar_servicio, nuevo_contrato,iniciar_sesion

import uvicorn
import os
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

app.include_router(admin.router)
app.include_router(consulta.router)
app.include_router(cancelar.router)
app.include_router(cancelar_servicio.router)
app.include_router(nuevo_contrato.router)
app.include_router(iniciar_sesion.router)


def clasificar(cc, referencia_p):
    try:
        connection = psycopg2.connect(**db_params)
        # Crear un cursor
        cursor = connection.cursor()

        # Obtener el ID de compra para la cédula dada
        query_id_compra = f"SELECT id_compra FROM compras WHERE cedula = '{cc}';"
        cursor.execute(query_id_compra)
        id_compra = cursor.fetchone()

        if id_compra:
            id_compra = id_compra[0]

            # Obtener el ID de producto para el nombre dado
            query_id_producto = f"SELECT id_producto FROM Producto WHERE Nombre = '{referencia_p}';"
            cursor.execute(query_id_producto)
            id_producto = cursor.fetchone()

            if id_producto:
                id_producto = id_producto[0]

                # Determinar la categoría del producto
                query_categoria = f"SELECT id_tipo_producto FROM Producto WHERE Nombre = '{referencia_p}';"
                cursor.execute(query_categoria)
                categoria_producto = cursor.fetchone()

                if categoria_producto:
                    categoria_producto = categoria_producto[0]

                    # Obtener la fecha actual
                    fecha_creacion = date.today()

                    # Calcular la fecha de expiración (un mes después)
                    fecha_expiracion = fecha_creacion + timedelta(days=30)

                    # Insertar en la tabla correspondiente según la categoría del producto
                    if categoria_producto == 1:  # Familiar
                        query_insert = f"""
                            INSERT INTO Familiar (id_compra, id_producto, fecha_creacion, fecha_expiracion, estado_cuenta, peticion)
                            VALUES ({id_compra}, {id_producto}, '{fecha_creacion}', '{fecha_expiracion}', 'Activando','Activando el producto');
                        """
                    elif categoria_producto == 2:  # Internet
                        query_insert = f"""
                            INSERT INTO Internet (id_compra, id_producto, fecha_creacion, fecha_expiracion, estado_cuenta, peticion)
                            VALUES ({id_compra}, {id_producto}, '{fecha_creacion}', '{fecha_expiracion}', 'Activando', 'Activando el producto');
                        """
                    elif categoria_producto == 3:  # Entretenimiento
                        query_insert = f"""
                            INSERT INTO Entretenimiento (id_compra, id_producto, fecha_creacion, fecha_expiracion, estado_cuenta, peticion)
                            VALUES ({id_compra}, {id_producto}, '{fecha_creacion}', '{fecha_expiracion}', 'Activando', 'Activando el producto');
                        """

                    # Ejecutar la consulta de inserción
                    cursor.execute(query_insert)

                    # Confirmar la transacción
                    connection.commit()

                    print("Datos insertados en la tabla correspondiente correctamente")

                else:
                    print("No se encontró la categoría del producto")

            else:
                print(f"No se encontró el ID de producto para el nombre '{referencia_p}'")

        else:
            print(f"No se encontró el ID de compra para la cédula '{cc}'")

    except Exception as e:
        print(f"Error al realizar la consulta: {e}")

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()



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

def guardar_compra(cedula, nombre, apellido, correo, departamento, ciudad_pueblo, barrio, celular, numero_tarjeta, fecha_expiracion, codigo_seguridad, contraseña):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        # Consulta SQL para insertar una nueva compra
        query = """
            INSERT INTO compras (
                cedula, nombre, apellido, correo, departamento, ciudad_pueblo,
                barrio, celular, numero_tarjeta, fecha_expiracion, codigo_seguridad, contraseña
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            cedula, nombre, apellido, correo, departamento, ciudad_pueblo,
            barrio, celular, numero_tarjeta, fecha_expiracion, codigo_seguridad, contraseña
        ))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error al registrar compra en la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor al procesar la compra")
# Ruta para manejar las solicitudes GET y POST a /comprarP
@app.route('/comprarP', methods=['GET', 'POST'])
async def comprar(request: Request):
    if request.method == 'POST':
        # Procesar la información del formulario si es una solicitud POST
        form_data = await request.form()
        cc = form_data['cc']
        nombre = form_data['nombre']
        apellido = form_data['apellido']
        email = form_data['email']
        departamento = form_data['departamento']
        ciudad_pueblo = form_data['ciudad_pueblo']
        barrio = form_data['barrio']
        celular = form_data['celular']
        numero_tarjeta = form_data['numero_tarjeta']
        fecha_expiracion = form_data['fecha_expiracion']
        codigo_seguridad = form_data['codigo_seguridad']
        contraseña = form_data['contraseña']
        plan_referencia = form_data['plan_referencia']
        if compra_ya_registrada(cc):
            return templates.TemplateResponse("comprar.html", {"request": request, "error": "Ya usted contrato el servicio", "success": None})
        else:
            # Registrar la compra en la base de datos
            guardar_compra(cc, nombre, apellido, email, departamento, ciudad_pueblo, barrio, celular, numero_tarjeta, fecha_expiracion, codigo_seguridad, contraseña)
            clasificar(cc, plan_referencia)
            return templates.TemplateResponse("comprar.html", {"request": request, "error": None, "success": "Compra registrada exitosamente"})

    elif request.method == 'GET':
        # Manejar la lógica si es una solicitud GET
        plan_referencia = request.query_params.get('plan_referencia')
        return templates.TemplateResponse("comprar.html", {"request": request, "error": None, "success": None, "plan_referencia": plan_referencia})

    # Manejar otras situaciones
    return templates.TemplateResponse("comprar.html", {"request": request, "error": "Error desconocido", "success": None, "plan_referencia": None})


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})
@app.get("/administrador", response_class=HTMLResponse)
def administrador(request: Request):
    return templates.TemplateResponse('inicio_sesion_admin.html', {"request": request})
@app.get("/listacompras", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('listacompras.html', {"request": request})
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
@app.get("/familiar", response_class=HTMLResponse)
def familiar(request: Request):
    return templates.TemplateResponse('familiar.html', {"request": request})
@app.get("/internet", response_class=HTMLResponse)
def familiar(request: Request):
    return templates.TemplateResponse('internet.html', {"request": request})
@app.get("/cobertura", response_class=HTMLResponse)
def cobertura(request: Request):
    return templates.TemplateResponse('cobertura.html', {"request": request})
@app.get("/inicio_sesion_admin", response_class=HTMLResponse)
def inicio_sesion_admin(request: Request):
    return templates.TemplateResponse('inicio_sesion_admin.html', {"request": request})
@app.get("/error", response_class=HTMLResponse)
def error(request: Request):
    return templates.TemplateResponse('error.html', {"request":request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))