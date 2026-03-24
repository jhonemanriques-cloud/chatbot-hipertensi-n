-- ============================================
-- BASE DE DATOS CHATBOT CONTROL HIPERTENSION
-- ============================================

CREATE DATABASE chatbot_hipertension;

USE chatbot_hipertension;

-- ============================================
-- TABLA PACIENTES
-- ============================================

CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT,
    genero VARCHAR(10),
    telefono VARCHAR(20),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLA MEDICOS
-- ============================================

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),
    correo VARCHAR(100)
);

-- ============================================
-- TABLA USUARIOS
-- ============================================

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    rol VARCHAR(20)
);

-- ============================================
-- TABLA SIGNOS VITALES
-- ============================================

CREATE TABLE signos_vitales (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT,
    presion_arterial VARCHAR(20),
    temperatura DECIMAL(4,2),
    saturacion_oxigeno INT,
    frecuencia_cardiaca INT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_paciente)
    REFERENCES pacientes(id_paciente)
);

-- ============================================
-- TABLA OBSERVACIONES MEDICAS
-- ============================================

CREATE TABLE observaciones_medicas (
    id_observacion INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT,
    id_medico INT,
    observacion TEXT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_paciente)
    REFERENCES pacientes(id_paciente),

    FOREIGN KEY (id_medico)
    REFERENCES medicos(id_medico)
);

-- ============================================
-- DATOS DE PRUEBA PACIENTES
-- ============================================

INSERT INTO pacientes (nombre, edad, genero, telefono)
VALUES
('Juan Perez', 55, 'Masculino', '3001234567'),
('Maria Lopez', 60, 'Femenino', '3109876543');

-- ============================================
-- DATOS DE PRUEBA MEDICOS
-- ============================================

INSERT INTO medicos (nombre, especialidad, correo)
VALUES
('Dr Carlos Ramirez', 'Cardiologia', 'carlos@hospital.com');

-- ============================================
-- DATOS DE PRUEBA USUARIOS
-- ============================================

INSERT INTO usuarios (usuario, password, rol)
VALUES
('admin', '123456', 'administrador'),
('medico1', '123456', 'medico'),
('paciente1', '123456', 'paciente');

-- ============================================
-- DATOS DE PRUEBA SIGNOS VITALES
-- ============================================

INSERT INTO signos_vitales 
(id_paciente, presion_arterial, temperatura, saturacion_oxigeno, frecuencia_cardiaca)
VALUES
(1, '120/80', 36.5, 98, 75),
(2, '140/90', 37.0, 96, 80);

-- ============================================
-- DATOS DE PRUEBA OBSERVACIONES MEDICAS
-- ============================================

INSERT INTO observaciones_medicas
(id_paciente, id_medico, observacion)
VALUES
(1, 1, 'Paciente con presión arterial controlada'),
(2, 1, 'Paciente debe realizar control semanal');

-- ============================================
-- CONSULTA DE REGISTROS
-- ============================================

SELECT 
p.nombre,
s.presion_arterial,
s.temperatura,
s.saturacion_oxigeno,
s.frecuencia_cardiaca,
s.fecha_registro
FROM signos_vitales s
JOIN pacientes p
ON s.id_paciente = p.id_paciente;

-- ============================================
-- EJEMPLO ELIMINAR REGISTRO
-- ============================================

-- DELETE FROM signos_vitales WHERE id_registro = 1;