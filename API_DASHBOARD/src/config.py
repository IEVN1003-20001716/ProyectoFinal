class DevelopmentConfig():
    DEBUG = True
   
    # Configuración para dashboard
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'dashboard'
   
    # Configuración para game
    GAME_MYSQL_HOST = '127.0.0.1'
    GAME_MYSQL_USER = 'root'
    GAME_MYSQL_PASSWORD = ''
    GAME_MYSQL_DB = 'game'
 
config = {
    'development': DevelopmentConfig
}