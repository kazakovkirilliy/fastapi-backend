from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

# DEBUG = config("DEBUG", cast=bool, default=False)
# TESTING = config("TESTING", cast=bool, default=False)

SECRET_KEY = config("SECRET_KEY", cast=Secret)
DATABASE_URL = config("DATABASE_URL")

# ADMIN_USERNAME = config("ADMIN_USERNAME")
# ADMIN_EMAIL = config("ADMIN_EMAIL", default='sklik.iva@firma.seznam.cz')
# ADMIN_PASSWORD = config("ADMIN_PASSWORD", cast=Secret)
