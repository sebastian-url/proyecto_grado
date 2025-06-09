
class Config():
    SECRET_KEY='ventas----de----avena-----'

#esta es la configuracion de la base de datos
class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'proyecto'
    MYSQL_PORT = 3306

config={
    'development':DevelopmentConfig,
}
