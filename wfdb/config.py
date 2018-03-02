class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "86b03e6b-02a4-501f-bc27-5021c38d87a5"


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    DEBUG = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    DEBUG = False
