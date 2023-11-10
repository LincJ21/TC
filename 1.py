import psycopg2

# Datos de configuración
pgdatabase = 'railway'
pghost = 'roundhouse.proxy.rlwy.net'
pgpassword = '5-5*GedCCGBaDfc2E4ea2bgcEb1*bD4*'
pgport = '42746'
pguser = 'postgres'

try:
    # Establecer la conexión a la base de datos
    connection = psycopg2.connect(
        dbname=pgdatabase,
        user=pguser,
        password=pgpassword,
        host=pghost,
        port=pgport
    )
    print("Conexión establecida")
    
    # Crear un cursor
    cursor = connection.cursor()

    # Datos que deseas insertar en la tabla Producto
    id_tipo_producto = 1
    Nombre = "Plan Familiar 1"
    Descripcion = "Adquiere nuestro combo familiar 1 con los siguientes beneficios: - 30 Megas de internet hogar - Telefonia fija ilimitada - Televisión ilimitada -"
    Precio = 40000

    # Consulta SQL para la inserción de datos
    query = """
    INSERT INTO Producto (id_tipo_producto, Nombre, descripcion, Precio)
    VALUES (%s, %s, %s, %s);
    """
    
    # Ejecutar la consulta
    cursor.execute(query, (id_tipo_producto, Nombre, Descripcion, Precio))

    # Confirmar la transacción
    connection.commit()

    # Cerrar el cursor y la conexión
    cursor.close()
    connection.close()
    print("Datos insertados en la tabla 'Producto' correctamente")

except Exception as e:
    print(f"Error al realizar la consulta: {e}")
