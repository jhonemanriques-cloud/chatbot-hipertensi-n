import mysql.connector

# ================================
# CONEXION A LA BASE DE DATOS
# ================================
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="J19h02o19n87+",
        database="chatbot_hipertension"
    )

conexion = conectar()
cursor = conexion.cursor()

# ================================
# FUNCIONES DEL CHATBOT
# ================================

def iniciar_sesion():
    """Valida las credenciales en la tabla 'usuarios' y retorna el rol"""
    print("\n" + "="*30)
    print("INICIO DE SESIÓN")
    print("="*30)
    
    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    sql = "SELECT rol FROM usuarios WHERE usuario = %s AND password = %s"
    valores = (usuario, password)

    try:
        cursor.execute(sql, valores)
        resultado = cursor.fetchone() # Trae solo la primera fila que coincida

        if resultado:
            rol = resultado[0] # Extraemos el texto del rol (ej: 'medico' o 'paciente')
            print(f"\n¡Bienvenido/a, {usuario}!")
            print(f" Rol identificado: {rol.upper()}")
            return rol
        else:
            print("\nError: Usuario o contraseña incorrectos.")
            return None

    except mysql.connector.Error as err:
        print(f"Error al consultar la base de datos: {err}")
        return None





def crear_paciente():
    """Registra un nuevo paciente y captura el ID autoincremental"""
    print("\n--- REGISTRO DE NUEVO PACIENTE ---")
    nombre = input("Nombre completo: ")
    edad = input("Edad: ")
    genero = input("Género (Masculino/Femenino): ")
    telefono = input("Teléfono: ")

    # SQL basado en tu estructura
    sql = "INSERT INTO pacientes (nombre, edad, genero, telefono) VALUES (%s, %s, %s, %s)"
    valores = (nombre, edad, genero, telefono)

    try:
        # 1. Ejecutamos la inserción
        cursor.execute(sql, valores)
        
        # 2. Confirmamos los cambios en la BD
        conexion.commit()
        
        # 3. Capturamos el ID inmediatamente después del commit
        nuevo_id = cursor.lastrowid 

        if nuevo_id:
            print("\n" + "="*30)
            print("¡PACIENTE CREADO EXITOSAMENTE!")
            print(f" EL ID ASIGNADO ES: {nuevo_id}")
            print("="*30)
            print("Importante: Use este ID para registrar signos vitales.")
        else:
            print(" El paciente se creó, pero no se pudo recuperar el ID.")

    except mysql.connector.Error as err:
        print(f"Error en la base de datos: {err}")
        # Si hay error, deshacemos cualquier cambio pendiente
        conexion.rollback()


def registrar_signos():
    """Registra signos vitales vinculados a un id_paciente"""
    id_paciente = input("Ingrese ID del paciente: ")
    presion = input("Ingrese presión arterial (ej: 120/80): ")
    temperatura = input("Ingrese temperatura (ej: 36.5): ")
    saturacion = input("Ingrese saturación de oxígeno (%): ")
    frecuencia = input("Ingrese frecuencia cardiaca (bpm): ")

    # El orden coincide con la tabla 'signos_vitales'
    sql = """
    INSERT INTO signos_vitales 
    (id_paciente, presion_arterial, temperatura, saturacion_oxigeno, frecuencia_cardiaca)
    VALUES (%s, %s, %s, %s, %s)
    """
    valores = (id_paciente, presion, temperatura, saturacion, frecuencia)

    try:
        cursor.execute(sql, valores)
        conexion.commit()
        print("Registro de signos vitales guardado correctamente.")
    except mysql.connector.Error as err:
        print(f"Error: Verifique que el ID del paciente sea correcto. {err}")


def consultar_registros(rol):
    """Consulta el historial filtrando por el rol del usuario"""
    
    # Lógica para PACIENTES: Solo ven su propia información
    if rol == 'paciente':
        id_paciente = input("Por favor, ingrese su ID de paciente: ")
        sql = """
        SELECT s.id_registro, p.nombre, s.presion_arterial, s.temperatura, 
               s.saturacion_oxigeno, s.frecuencia_cardiaca, s.fecha_registro
        FROM signos_vitales s
        JOIN pacientes p ON s.id_paciente = p.id_paciente
        WHERE s.id_paciente = %s
        """
        valores = (id_paciente,)

    # Lógica para MÉDICOS/ADMINS: Ven todo o filtran por paciente
    else:
        print("\nOpciones de consulta médica:")
        print("1. Ver historial de todos los pacientes")
        print("2. Buscar por ID de un paciente específico")
        opc = input("Seleccione: ")
        
        if opc == "2":
            id_paciente = input("Ingrese el ID del paciente a buscar: ")
            sql = """
            SELECT s.id_registro, p.nombre, s.presion_arterial, s.temperatura, s.saturacion_oxigeno, 
                   s.frecuencia_cardiaca, s.fecha_registro
            FROM signos_vitales s
            JOIN pacientes p ON s.id_paciente = p.id_paciente
            WHERE s.id_paciente = %s
            """
            valores = (id_paciente,)
        else:
            # Consulta general sin filtro WHERE
            sql = """
            SELECT s.id_registro, p.nombre, s.presion_arterial, s.temperatura, s.saturacion_oxigeno, 
                   s.frecuencia_cardiaca, s.fecha_registro
            FROM signos_vitales s
            JOIN pacientes p ON s.id_paciente = p.id_paciente
            """
            valores = ()

    # Ejecución de la consulta a la base de datos
    try:
        if valores:
            cursor.execute(sql, valores)
        else:
            cursor.execute(sql)
            
        resultados = cursor.fetchall()

        if not resultados:
            print("\n No se encontraron registros de signos vitales.")
            return

        print("\n--- HISTORIAL DE SIGNOS VITALES ---")
        for fila in resultados:
            print(f"ID Registro: {fila[0]} | Paciente: {fila[1]} | PA: {fila[2]} | T: {fila[3]}°C | SatO2: {fila[4]}% | FC: {fila[5]} bpm | Fecha: {fila[6]}")
        print("-----------------------------------")
        
    except mysql.connector.Error as err:
        print(f"Error al consultar la base de datos: {err}")




def agregar_observacion():
    """Permite al médico dejar comentarios en la tabla 'observaciones_medicas'"""
    id_paciente = input("Ingrese ID del paciente: ")
    id_medico = input("Ingrese ID del médico: ")
    observacion = input("Ingrese observación médica: ")

    sql = "INSERT INTO observaciones_medicas (id_paciente, id_medico, observacion) VALUES (%s, %s, %s)"
    valores = (id_paciente, id_medico, observacion)

    cursor.execute(sql, valores)
    conexion.commit()
    print("Observación registrada correctamente.")



def eliminar_registro(rol):
    """Permite a un paciente eliminar un registro propio"""
    
    # 3. Validar permisos: Solo los pacientes pueden eliminar
    if rol != 'paciente':
        print("\n Acceso denegado: Esta función es exclusiva para pacientes.")
        return

    print("\n--- ELIMINAR REGISTRO INCONGRUENTE ---")
    
    # 2. Lógica de selección: Pedimos credenciales y el ID del registro a borrar
    id_paciente = input("Por seguridad, confirme su ID de paciente: ")
    id_registro = input("Ingrese el ID del registro que desea eliminar: ")

    # Consulta para verificar que el registro exista Y le pertenezca a este paciente
    sql_verificar = "SELECT id_registro FROM signos_vitales WHERE id_registro = %s AND id_paciente = %s"
    valores_verificar = (id_registro, id_paciente)

    try:
        cursor.execute(sql_verificar, valores_verificar)
        resultado = cursor.fetchone()

        # 4. Actualizar base de datos tras la eliminación
        if resultado:
            # Si el registro le pertenece, ejecutamos el comando DELETE
            sql_borrar = "DELETE FROM signos_vitales WHERE id_registro = %s"
            cursor.execute(sql_borrar, (id_registro,))
            conexion.commit() # Confirmamos los cambios en MySQL
            
            print("\n¡Registro eliminado correctamente de la base de datos!")
        else:
            print("\n Error: El registro no existe o no le pertenece a su usuario.")
            
    except mysql.connector.Error as err:
        print(f"\nError en la base de datos al intentar eliminar: {err}")


# ================================
# MENU DEL CHATBOT
# ================================

def menu(rol):
    """Menú dinámico basado en el rol del usuario logueado"""
    while True:
        print("\n" + "="*40)
        print(" MENÚ PRINCIPAL - CONTROL HIPERTENSIÓN")
        print("="*40)

        # Opciones exclusivas para pacientes 
        if rol == 'paciente':
            print("1. Registrar mis signos vitales")
            print("2. Consultar mi historial")
            print("3. Eliminar un registro incongruente")
            print("4. Cerrar sesión")
            
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                registrar_signos()
            elif opcion == "2":
                consultar_registros(rol)
            elif opcion == "3":
                eliminar_registro(rol)
            elif opcion == "4":
                print("Cerrando sesión... ¡Hasta pronto!")
                break
            else:
                print(" Opción no válida.")

        # Opciones exclusivas para médicos y administradores 
        elif rol in ['medico', 'administrador']:
            print("1. Crear nuevo paciente")
            print("2. Consultar registros de pacientes")
            print("3. Agregar observación médica")
            print("4. Cerrar sesión")
            
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                crear_paciente()
            elif opcion == "2":
                consultar_registros(rol)
            elif opcion == "3":
                agregar_observacion()
            elif opcion == "4":
                print("Cerrando sesión... ¡Hasta pronto!")
                break
            else:
                print(" Opción no válida.")

# ================================
# EJECUCION DEL CHATBOT
# ================================

if __name__ == "__main__":
    rol_actual = None
    
    # Bucle para obligar al usuario a iniciar sesión correctamente
    while rol_actual is None:
        rol_actual = iniciar_sesion()
    
    # Pasamos el rol capturado al menú dinámico
    menu(rol_actual) 
    
    cursor.close()
    conexion.close()