# utils.py
import psycopg2
from fastapi import HTTPException, Request
from fastapi.templating import Jinja2Templates
from datetime import date, timedelta# main.py

db_params = {
    'host': 'roundhouse.proxy.rlwy.net',
    'user': 'postgres',
    'password': '5-5*GedCCGBaDfc2E4ea2bgcEb1*bD4*',
    'database': 'railway',
    'port': 42746
}
templates = Jinja2Templates(directory="templates")


def autenticar_administrador(codigo: str, contraseña: str):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            query = "SELECT * FROM administradores WHERE codigo = %s AND contraseña = %s"
            cursor.execute(query, (codigo, contraseña))
            administrador = cursor.fetchone()

            return administrador is not None

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al autenticar administrador: {e}")

def Tabla(request: Request):
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

def consultar_productos(cc: str):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            query_id_compra = f"SELECT id_compra FROM compras WHERE cedula = '{cc}';"
            cursor.execute(query_id_compra)
            id_compra = cursor.fetchone()

            if id_compra:
                id_compra = id_compra[0]

                query_familiar = f"""
                    SELECT c.id_compra, c.cedula, c.nombre, c.apellido, f.id_producto, p.nombre AS nombre_producto,
                        p.descripcion, p.precio, f.fecha_creacion, f.fecha_expiracion, f.estado_cuenta
                    FROM compras c
                    INNER JOIN Familiar f ON c.id_compra = f.id_compra
                    INNER JOIN Producto p ON f.id_producto = p.id_producto
                    WHERE c.id_compra = {id_compra};
                """

                cursor.execute(query_familiar)
                productos_familiar = cursor.fetchall()

                query_internet = f"""
                    SELECT c.id_compra, c.cedula, c.nombre, c.apellido, f.id_producto, p.nombre AS nombre_producto,
                        p.descripcion, p.precio, f.fecha_creacion, f.fecha_expiracion, f.estado_cuenta
                    FROM compras c
                    INNER JOIN Internet f ON c.id_compra = f.id_compra
                    INNER JOIN Producto p ON f.id_producto = p.id_producto
                    WHERE c.id_compra = {id_compra};
                """
                cursor.execute(query_internet)
                productos_internet = cursor.fetchall()

                query_entretenimiento = f"""
                    SELECT c.id_compra, c.cedula, c.nombre, c.apellido, f.id_producto, p.nombre AS nombre_producto,
                        p.descripcion, p.precio, f.fecha_creacion, f.fecha_expiracion, f.estado_cuenta
                    FROM compras c
                    INNER JOIN Entretenimiento f ON c.id_compra = f.id_compra
                    INNER JOIN Producto p ON f.id_producto = p.id_producto
                    WHERE c.id_compra = {id_compra};
                """
                cursor.execute(query_entretenimiento)
                productos_entretenimiento = cursor.fetchall()

                return productos_familiar, productos_internet, productos_entretenimiento

            else:
                raise HTTPException(status_code=404, detail=f"No se encontró el ID de compra para la cédula '{cc}'")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la consulta: {e}")


def autenticar_administrador(codigo: str, contraseña: str):
    try:
        with psycopg2.connect(**db_params) as connection, connection.cursor() as cursor:
            query = "SELECT * FROM administradores WHERE codigo = %s AND contraseña = %s"
            cursor.execute(query, (codigo, contraseña))
            administrador = cursor.fetchone()

            return administrador is not None

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al autenticar administrador: {e}")

def clasificar(cc, referencia_p):
    try:
        connection = psycopg2.connect(**db_params)
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
