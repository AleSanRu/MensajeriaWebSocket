from pydantic import BaseSettings

class Settings(BaseSettings):
    # Conexión completa con mongo 27017
    mongodb_uri: str = "mongodb://localhost:27017/messaging_db"
    
    # Nombre de la BD este o lo crea o lo utilizar 1 de 2 
    mongodb_name: str = "messaging_db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    def __init__(self, **values):
        super().__init__(**values)
        # Extrae el nombre de la BD de la URI si está presente
        if '/' in self.mongodb_uri.split('://')[1]:
            self.mongodb_name = self.mongodb_uri.split('/')[-1].split('?')[0]

settings = Settings()