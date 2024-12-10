from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SERVER = os.getenv('SERVER')
DATABASE = os.getenv('DATABASE')

DATABASE_CONFIG = {
    'DRIVER': '{ODBC Driver 17 for SQL Server}',
    'SERVER': SERVER,
    'DATABASE': DATABASE,
    'Trusted_Connection': 'yes',
    'TrustServerCertificate': 'yes',
}
