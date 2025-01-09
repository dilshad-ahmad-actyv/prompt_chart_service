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

# AWS S3 Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')