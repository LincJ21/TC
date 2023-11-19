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

    # Añadir la columna "petición" a la tabla "Familiar"
    query_add_peticion_column_familiar = """
    CREATE TABLE Administradores (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(255) NOT NULL,
    contraseña VARCHAR(255) NOT NULL
    );

    """
    cursor.execute(query_add_peticion_column_familiar)

    # Confirmar la transacción
    connection.commit()

    # Cerrar el cursor y la conexión
    cursor.close()
    connection.close()
    print("todo correcto")

except Exception as e:
    print(f"Error al realizar la consulta: {e}")
