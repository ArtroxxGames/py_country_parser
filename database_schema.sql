-- Archivo: database_schema.sql
-- Script para crear las tablas necesarias en PostgreSQL

-- Crear el esquema si no existe
CREATE SCHEMA IF NOT EXISTS identidades;

-- Tabla de departamentos
CREATE TABLE IF NOT EXISTS identidades.departamentos (
    id SERIAL PRIMARY KEY,
    codigo INTEGER UNIQUE NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL
);

-- Índices para departamentos
CREATE INDEX IF NOT EXISTS idx_departamentos_codigo ON identidades.departamentos(codigo);
CREATE INDEX IF NOT EXISTS idx_departamentos_deleted_at ON identidades.departamentos(deleted_at);

-- Tabla de ciudades
CREATE TABLE IF NOT EXISTS identidades.ciudades (
    id SERIAL PRIMARY KEY,
    codigo INTEGER NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    area INTEGER,
    departamento_id INTEGER REFERENCES identidades.departamentos(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL,
    UNIQUE(codigo, departamento_id)
);

-- Índices para ciudades
CREATE INDEX IF NOT EXISTS idx_ciudades_codigo ON identidades.ciudades(codigo);
CREATE INDEX IF NOT EXISTS idx_ciudades_departamento_id ON identidades.ciudades(departamento_id);
CREATE INDEX IF NOT EXISTS idx_ciudades_deleted_at ON identidades.ciudades(deleted_at);

-- Tabla de barrios
CREATE TABLE IF NOT EXISTS identidades.barrios (
    id SERIAL PRIMARY KEY,
    codigo INTEGER NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    ciudad_id INTEGER REFERENCES identidades.ciudades(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP NULL,
    UNIQUE(codigo, ciudad_id)
);

-- Índices para barrios
CREATE INDEX IF NOT EXISTS idx_barrios_codigo ON identidades.barrios(codigo);
CREATE INDEX IF NOT EXISTS idx_barrios_ciudad_id ON identidades.barrios(ciudad_id);
CREATE INDEX IF NOT EXISTS idx_barrios_deleted_at ON identidades.barrios(deleted_at);

-- Comentarios en las tablas
COMMENT ON TABLE identidades.departamentos IS 'Tabla de departamentos de Paraguay';
COMMENT ON TABLE identidades.ciudades IS 'Tabla de ciudades/distritos de Paraguay';
COMMENT ON TABLE identidades.barrios IS 'Tabla de barrios/localidades de Paraguay';

-- Comentarios en las columnas importantes
COMMENT ON COLUMN identidades.departamentos.codigo IS 'Código único del departamento';
COMMENT ON COLUMN identidades.ciudades.area IS 'Código de área de la ciudad';
COMMENT ON COLUMN identidades.ciudades.departamento_id IS 'Referencia al departamento padre';
COMMENT ON COLUMN identidades.barrios.ciudad_id IS 'Referencia a la ciudad padre';

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para actualizar updated_at
CREATE TRIGGER update_departamentos_updated_at BEFORE UPDATE ON identidades.departamentos 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ciudades_updated_at BEFORE UPDATE ON identidades.ciudades 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_barrios_updated_at BEFORE UPDATE ON identidades.barrios 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
