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

    # Consulta SQL para modificar las columnas "CC" y "Contraseña" a tipo VARCHAR
    query = """
    ALTER TABLE usuarios
    ALTER COLUMN CC TYPE VARCHAR(255),
    ALTER COLUMN TELEFONO TYPE VARCHAR(255);
    """
    
    # Ejecutar la consulta
    cursor.execute(query)

    # Confirmar la transacción
    connection.commit()

    # Cerrar el cursor y la conexión
    cursor.close()
    connection.close()
    print("Columnas 'CC' y 'Contraseña' modificadas a tipo VARCHAR correctamente")

except Exception as e:
    print(f"Error al realizar la consulta: {e}")
