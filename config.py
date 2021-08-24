import os 

class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = '<Flask WTF Secret Key>'
    QUOTE_URL = "http://quotes.stormconsultancy.co.uk/random.json"
    
    #  email configurations
    MAIL_SERVER = 'smtp.gmail.com' 
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "kalambanidouglas@gmail.com"
    MAIL_PASSWORD ="kelvin97"   
    MAIL_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:kkkk@localhost/blog'
  
 

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