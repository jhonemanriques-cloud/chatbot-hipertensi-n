import mysql.connector
from mysql.connector import Error

# ================================
# CONEXION A LA BASE DE DATOS
# ================================
def conectar():
    """Crea y retorna una conexión a la base de datos."""
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="J19h02o19n87+",
            database="chatbot_hipertension"
        )
        return conexion
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# ================================
# FUNCIONES DE APOYO
# ================================
def ejecutar_consulta(sql, valores=None, fetch=False):
    """Ejecuta consultas SQL de manera segura y opcionalmente retorna resultados."""
    conexion = conectar()
    if not conexion:
        return None
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, valores)
            if fetch:
                return cursor.fetchall()
            conexion.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error en la consulta SQL: {e}")
        conexion.rollback()
        return None
    finally:
        conexion.close()

def input_no_vacio(prompt):
    """Solicita input al usuario hasta que no esté vacío."""
    valor = ""
    while not valor.strip():
        valor = input(prompt)
    return valor.strip()

# ================================
# FUNCIONES DEL CHATBOT
# ================================
def iniciar_sesion():
    """Valida las credenciales y retorna el rol."""
    print("\n" + "="*30)
    print("INICIO DE SESIÓN")
    print("="*30)

    usuario = input_no_vacio("Usuario: ")
    password = input_no_vacio("Contraseña: ")

    sql = "SELECT rol FROM usuarios WHERE usuario = %s AND password = %s"
    resultado = ejecutar_consulta(sql, (usuario, password), fetch=True)

    if resultado:
        rol = resultado[0][0]
        print(f"\n¡Bienvenido/a, {usuario}!")
        print(f" Rol identificado: {rol.upper()}")
        return rol
    else:
        print("\nError: Usuario o contraseña incorrectos.")
        return None

def crear_paciente():
    """Registra un nuevo paciente y muestra su ID."""
    print("\n--- REGISTRO DE NUEVO PACIENTE ---")
    nombre = input_no_vacio("Nombre completo: ")
    edad = input_no_vacio("Edad: ")
    genero = input_no_vacio("Género (Masculino/Femenino): ")
    telefono = input_no_vacio("Teléfono: ")

    sql = "INSERT INTO pacientes (nombre, edad, genero, telefono) VALUES (%s, %s, %s, %s)"
    nuevo_id = ejecutar_consulta(sql, (nombre, edad, genero, telefono))

    if nuevo_id:
        print("\n" + "="*30)
        print("¡PACIENTE CREADO EXITOSAMENTE!")
        print(f" ID ASIGNADO: {nuevo_id}")
        print("="*30)
    else:
        print("No se pudo crear el paciente.")

def registrar_signos():
    """Registra signos vitales de un paciente."""
    id_paciente = input_no_vacio("Ingrese ID del paciente: ")
    presion = input_no_vacio("Ingrese presión arterial (ej: 120/80): ")
    temperatura = input_no_vacio("Ingrese temperatura (ej: 36.5): ")
    saturacion = input_no_vacio("Ingrese saturación de oxígeno (%): ")
    frecuencia = input_no_vacio("Ingrese frecuencia cardiaca (bpm): ")

    sql = """
    INSERT INTO signos_vitales 
    (id_paciente, presion_arterial, temperatura, saturacion_oxigeno, frecuencia_cardiaca)
    VALUES (%s, %s, %s, %s, %s)
    """
    if ejecutar_consulta(sql, (id_paciente, presion, temperatura, saturacion, frecuencia)):
        print("Registro de signos vitales guardado correctamente.")

def consultar_registros(rol):
    """Consulta signos vitales según el rol."""
    sql_base = """
    SELECT s.id_registro, p.nombre, s.presion_arterial, s.temperatura,
           s.saturacion_oxigeno, s.frecuencia_cardiaca, s.fecha_registro
    FROM signos_vitales s
    JOIN pacientes p ON s.id_paciente = p.id_paciente
    """
    valores = ()
    
    if rol == 'paciente':
        id_paciente = input_no_vacio("Ingrese su ID de paciente: ")
        sql_base += " WHERE s.id_paciente = %s"
        valores = (id_paciente,)
    else:
        print("\nOpciones de consulta médica:")
        print("1. Ver historial de todos los pacientes")
        print("2. Buscar por ID de un paciente")
        opc = input("Seleccione: ")
        if opc == "2":
            id_paciente = input_no_vacio("Ingrese ID del paciente: ")
            sql_base += " WHERE s.id_paciente = %s"
            valores = (id_paciente,)

    resultados = ejecutar_consulta(sql_base, valores, fetch=True)
    if not resultados:
        print("\nNo se encontraron registros.")
        return

    print("\n--- HISTORIAL DE SIGNOS VITALES ---")
    for fila in resultados:
        print(f"ID Registro: {fila[0]} | Paciente: {fila[1]} | PA: {fila[2]} | "
              f"T: {fila[3]}°C | SatO2: {fila[4]}% | FC: {fila[5]} bpm | Fecha: {fila[6]}")
    print("-----------------------------------")

def agregar_observacion():
    """Agrega observaciones médicas para un paciente."""
    id_paciente = input_no_vacio("ID del paciente: ")
    id_medico = input_no_vacio("ID del médico: ")
    observacion = input_no_vacio("Observación: ")

    sql = "INSERT INTO observaciones_medicas (id_paciente, id_medico, observacion) VALUES (%s, %s, %s)"
    if ejecutar_consulta(sql, (id_paciente, id_medico, observacion)):
        print("Observación registrada correctamente.")

def eliminar_registro(rol):
    """Permite eliminar un registro propio de signos vitales."""
    if rol != 'paciente':
        print("\nAcceso denegado: Solo pacientes pueden eliminar registros.")
        return

    id_paciente = input_no_vacio("Confirme su ID de paciente: ")
    id_registro = input_no_vacio("ID del registro a eliminar: ")

    sql_verificar = "SELECT id_registro FROM signos_vitales WHERE id_registro = %s AND id_paciente = %s"
    resultado = ejecutar_consulta(sql_verificar, (id_registro, id_paciente), fetch=True)

    if resultado:
        sql_borrar = "DELETE FROM signos_vitales WHERE id_registro = %s"
        if ejecutar_consulta(sql_borrar, (id_registro,)):
            print("Registro eliminado correctamente.")
    else:
        print("El registro no existe o no pertenece al paciente.")

# ================================
# MENU DEL CHATBOT
# ================================
def menu(rol):
    while True:
        print("\n" + "="*40)
        print(" MENÚ PRINCIPAL - CONTROL HIPERTENSIÓN")
        print("="*40)

        if rol == 'paciente':
            opciones = {
                "1": registrar_signos,
                "2": lambda: consultar_registros(rol),
                "3": lambda: eliminar_registro(rol),
                "4": exit
            }
            print("1. Registrar mis signos vitales")
            print("2. Consultar mi historial")
            print("3. Eliminar un registro incongruente")
            print("4. Cerrar sesión")
        else:
            opciones = {
                "1": crear_paciente,
                "2": lambda: consultar_registros(rol),
                "3": agregar_observacion,
                "4": exit
            }
            print("1. Crear nuevo paciente")
            print("2. Consultar registros de pacientes")
            print("3. Agregar observación médica")
            print("4. Cerrar sesión")

        opcion = input("Seleccione una opción: ")
        accion = opciones.get(opcion)
        if accion:
            accion()
        else:
            print("Opción no válida.")

# ================================
# EJECUCIÓN DEL CHATBOT
# ================================
if __name__ == "__main__":
    rol_actual = None
    while rol_actual is None:
        rol_actual = iniciar_sesion()
    menu(rol_actual)
