
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_host: str 
    database_password:str
    database_name:str 
    database_username: str 
    algorithm: str 
    secret_key:str
    
    

    class Config:
        env_file = ".env"

settings = Settings()