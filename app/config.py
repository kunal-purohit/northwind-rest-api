class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/northwind_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config_by_name = {"dev": DevelopmentConfig, "test": TestingConfig}
