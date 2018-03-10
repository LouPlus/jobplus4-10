import os
class BaseConfig(object):
    '''p配置基类'''
    SECRET_KEY='make sure to set a very secret key'
    ADMIN_PER_PAGE=10
    INDEX_PER_PAGE=9
    UPLOADED_PHOTO_FILE=os.getcwd()
    UPLOADED_RESUME_FILE=os.getcwd()
class DevelopmentConfig(BaseConfig):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8'

class ProductionConfig(BaseConfig):
    pass
class TestingConfig(BaseConfig):
    pass

configs={
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'testing':TestingConfig
}

