from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

# DEBUG = config("DEBUG", cast=bool, default=False)
# TESTING = config("TESTING", cast=bool, default=False)

SECRET_KEY = config("SECRET_KEY", cast=Secret)

DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD", cast=Secret)
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME")


# ADMIN_USERNAME = config("ADMIN_USERNAME")
# ADMIN_EMAIL = config("ADMIN_EMAIL", default='sklik.iva@firma.seznam.cz')
# ADMIN_PASSWORD = config("ADMIN_PASSWORD", cast=Secret)
