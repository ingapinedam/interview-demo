"""
Configuración de base de datos para el Agente Entrevistador
Maneja tanto SQLite como PostgreSQL
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class DatabaseConfig:
    """Configuración de base de datos"""

    # Tipo de base de datos: 'sqlite' o 'postgresql'
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')

    # Configuración SQLite (modo legacy)
    SQLITE_PATH = os.getenv('SQLITE_PATH', 'preguntas_entrevista.db')

    # Configuración PostgreSQL
    POSTGRES_CONFIG = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5432'),
        'database': os.getenv('POSTGRES_DB', 'preguntas_entrevista'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'password'),
    }

    @classmethod
    def get_postgres_connection_string(cls):
        """Genera string de conexión para PostgreSQL"""
        config = cls.POSTGRES_CONFIG
        return f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

    @classmethod
    def get_postgres_connection_params(cls):
        """Retorna parámetros de conexión para psycopg2"""
        return cls.POSTGRES_CONFIG

    @classmethod
    def is_postgresql(cls):
        """Verifica si se usa PostgreSQL"""
        return cls.DATABASE_TYPE.lower() == 'postgresql'

    @classmethod
    def is_sqlite(cls):
        """Verifica si se usa SQLite"""
        return cls.DATABASE_TYPE.lower() == 'sqlite'