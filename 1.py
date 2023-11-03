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

    # Crear un cursor para ejecutar consultas SQL
    cursor = connection.cursor()

    # Sentencia SQL para crear la tabla "usuarios" con una clave primaria autoincremental
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        cc VARCHAR(255) UNIQUE,
        name VARCHAR(255),
        ape VARCHAR(255),
        cell VARCHAR(15),
        email VARCHAR(255),
        password VARCHAR(255)
    )
    '''

    cursor.execute(create_table_query)
    connection.commit()

    print("Tabla 'usuarios' creada o ya existente")

    # Cerrar el cursor y la conexión
    cursor.close()
    connection.close()

except Exception as e:
    print(f"Error al crear la tabla 'usuarios': {e}")
