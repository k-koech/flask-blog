import os 

class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = '<Flask WTF Secret Key>'
    QUOTE_URL = "http://quotes.stormconsultancy.co.uk/random.json"

    EMAIL = "kalambanidouglas@gmail.com"
    PASSWORD = "kalambani97?"
  
class TestConfig(Config):
    pass


class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    

class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:kkkk@localhost/blog'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}