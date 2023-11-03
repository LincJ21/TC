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
    cursor = connection.cursor()

    # Cambia el número de cédula que deseas buscar (en este caso, se usa 1234567890 como ejemplo)
    cedula = '1234567890'

    # Cambia la consulta SQL para buscar un usuario por número de cédula
    query = "SELECT * FROM usuarios WHERE cc = %s"
    cursor.execute(query, (cedula,))

    # Obtén el resultado
    user = cursor.fetchone()

    if user:
        # Imprime los datos del usuario
        print(f"ID: {user[0]}")
        print(f"Cédula: {user[1]}")
        print(f"Nombre: {user[2]}")
        print(f"Apellido: {user[3]}")
        print(f"Email: {user[4]}")

    else:
        print("Usuario no encontrado")

    cursor.close()
    connection.close()

except Exception as e:
    print(f"Error al realizar la consulta: {e}")
