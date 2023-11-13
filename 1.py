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

    # Sentencia SQL para crear la tabla compras
    create_table_query = """
    CREATE TABLE compras (
        id_compra serial PRIMARY KEY,
        cedula VARCHAR(255),
        nombre VARCHAR(255),
        apellido VARCHAR(255),
        correo VARCHAR(255),
        departamento VARCHAR(255),
        ciudad_pueblo VARCHAR(255),
        barrio VARCHAR(255),
        celular VARCHAR(15),
        numero_tarjeta VARCHAR(255),
        fecha_expiracion VARCHAR(7),
        codigo_seguridad VARCHAR(3)
    );
    """
    
    # Ejecutar la consulta
    cursor.execute(create_table_query)

    # Confirmar la transacción
    connection.commit()

    # Cerrar el cursor y la conexión
    cursor.close()
    connection.close()
    print("Tabla 'compras' creada correctamente")

except Exception as e:
    print(f"Error al crear la tabla 'compras': {e}")

