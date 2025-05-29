import csv
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Configurar logging para debug
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cargar_datos_geograficos(archivo_csv, conexion_db):
    """
    Carga datos geográficos desde CSV a las tablas de departamentos, ciudades y barrios
    """
    
    # Diccionarios para evitar duplicados y mantener referencias
    departamentos_cache = {}
    ciudades_cache = {}
    
    # Contadores para estadísticas
    filas_procesadas = 0
    errores = 0
    
    try:
        with open(archivo_csv, 'r', encoding='latin-1') as file:
            # Leer el CSV con delimitador punto y coma
            reader = csv.reader(file, delimiter=';')
            
            # Saltar la primera línea si es header
            header = next(reader, None)
            logger.info(f"Procesando archivo CSV con header: {header}")
            
            with conexion_db.cursor(cursor_factory=RealDictCursor) as cursor:
                for row_num, row in enumerate(reader, start=2):  # Start=2 porque line 1 es header
                    try:
                        if len(row) < 8:  # Verificar que tenga todas las columnas
                            logger.warning(f"Fila {row_num}: Datos insuficientes, saltando")
                            continue
                            
                        # Extraer datos de la fila con validación
                        try:
                            codigo_departamento = int(row[1].strip())
                            desc_departamento = row[2].strip()
                            codigo_distrito = int(row[3].strip())
                            desc_distrito = row[4].strip()
                            area = int(row[5].strip())
                            codigo_barrio = int(row[6].strip())
                            desc_barrio = row[7].strip()
                        except (ValueError, IndexError) as e:
                            logger.error(f"Fila {row_num}: Error en formato de datos: {e}")
                            errores += 1
                            continue
                        
                        # Validar que las descripciones no estén vacías
                        if not desc_departamento or not desc_distrito or not desc_barrio:
                            logger.warning(f"Fila {row_num}: Descripciones vacías, saltando")
                            continue
                        
                        # 1. Insertar/obtener departamento
                        dept_key = (codigo_departamento, desc_departamento)
                        if dept_key not in departamentos_cache:
                            try:
                                cursor.execute("""
                                    INSERT INTO identidades.departamentos (codigo, descripcion)
                                    VALUES (%s, %s)
                                    ON CONFLICT (codigo) DO UPDATE SET 
                                        descripcion = EXCLUDED.descripcion,
                                        updated_at = NOW()
                                    RETURNING id
                                """, (codigo_departamento, desc_departamento))
                                
                                result = cursor.fetchone()
                                if result:
                                    dept_id = result['id']
                                    departamentos_cache[dept_key] = dept_id
                                else:
                                    logger.error(f"Fila {row_num}: No se pudo obtener ID del departamento")
                                    errores += 1
                                    continue
                            except psycopg2.Error as e:
                                logger.error(f"Fila {row_num}: Error insertando departamento: {e}")
                                errores += 1
                                continue
                        else:
                            dept_id = departamentos_cache[dept_key]
                        
                        # 2. Insertar/obtener ciudad
                        ciudad_key = (codigo_distrito, desc_distrito, codigo_departamento)
                        if ciudad_key not in ciudades_cache:
                            try:
                                cursor.execute("""
                                    INSERT INTO identidades.ciudades (codigo, descripcion, area, departamento_id)
                                    VALUES (%s, %s, %s, %s)
                                    ON CONFLICT (codigo, departamento_id) DO UPDATE SET 
                                        descripcion = EXCLUDED.descripcion,
                                        area = EXCLUDED.area,
                                        updated_at = NOW()
                                    RETURNING id
                                """, (codigo_distrito, desc_distrito, area, dept_id))
                                
                                result = cursor.fetchone()
                                if result:
                                    ciudad_id = result['id']
                                    ciudades_cache[ciudad_key] = ciudad_id
                                else:
                                    logger.error(f"Fila {row_num}: No se pudo obtener ID de la ciudad")
                                    errores += 1
                                    continue
                            except psycopg2.Error as e:
                                logger.error(f"Fila {row_num}: Error insertando ciudad: {e}")
                                errores += 1
                                continue
                        else:
                            ciudad_id = ciudades_cache[ciudad_key]
                        
                        # 3. Insertar barrio
                        try:
                            cursor.execute("""
                                INSERT INTO identidades.barrios (codigo, descripcion, ciudad_id)
                                VALUES (%s, %s, %s)
                                ON CONFLICT (codigo, ciudad_id) DO UPDATE SET 
                                    descripcion = EXCLUDED.descripcion,
                                    updated_at = NOW()
                            """, (codigo_barrio, desc_barrio, ciudad_id))
                        except psycopg2.Error as e:
                            logger.error(f"Fila {row_num}: Error insertando barrio: {e}")
                            errores += 1
                            continue
                        
                        filas_procesadas += 1
                        
                        # Commit cada 100 registros para evitar transacciones muy largas
                        if filas_procesadas % 100 == 0:
                            conexion_db.commit()
                            logger.info(f"Procesadas {filas_procesadas} filas...")
                            
                    except Exception as e:
                        logger.error(f"Fila {row_num}: Error inesperado: {e}")
                        errores += 1
                        continue
                
                # Commit final
                conexion_db.commit()
                
                # Mostrar estadísticas de la carga
                logger.info("=== ESTADÍSTICAS DE CARGA ===")
                logger.info(f"Filas procesadas exitosamente: {filas_procesadas}")
                logger.info(f"Errores encontrados: {errores}")
                logger.info("Datos cargados exitosamente!")
                
    except FileNotFoundError:
        logger.error(f"No se pudo encontrar el archivo: {archivo_csv}")
        raise
    except Exception as e:
        logger.error(f"Error general en la carga: {e}")
        conexion_db.rollback()
        raise

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar conexión a la base de datos
    # IMPORTANTE: Actualiza estas credenciales con las tuyas
    # Para mayor seguridad, considera usar variables de entorno
    conexion = psycopg2.connect(
        host="localhost",           # Cambia por tu host
        database="tu_database",     # Cambia por tu database  
        user="tu_usuario",         # Cambia por tu usuario
        password="tu_password",    # Cambia por tu password
        port=5432,                 # Puerto de PostgreSQL
        connect_timeout=30         # Timeout de 30 segundos
    )
    
    try:
        logger.info("Iniciando carga de datos geográficos...")
        
        # Cargar los datos
        cargar_datos_geograficos("./datos.csv", conexion)
        
        # Mostrar estadísticas
        with conexion.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM identidades.departamentos WHERE deleted_at IS NULL")
            dept_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM identidades.ciudades WHERE deleted_at IS NULL")
            ciudad_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM identidades.barrios WHERE deleted_at IS NULL")
            barrio_count = cursor.fetchone()[0]
            
            logger.info("=== ESTADÍSTICAS FINALES ===")
            logger.info(f"Departamentos: {dept_count}")
            logger.info(f"Ciudades: {ciudad_count}")
            logger.info(f"Barrios: {barrio_count}")
            
    except Exception as e:
        logger.error(f"Error: {e}")
        conexion.rollback()
    finally:
        conexion.close()
        logger.info("Conexión cerrada.")
