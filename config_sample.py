class Config:
    SECRET_KEY = '709bb33e1d3b513e4a9ee78a2a940063'

    TESTING = True
    DEBUG = True

    # DRIVER = 'postgresql'
    # USER = 'postgres'
    # PASSWORD = ''
    # HOST = 'localhost'
    # BD_HML = 'lancheriaHML'
    # BD_PRD = 'lancheriaPRD'

    # SQLALCHEMY_DATABASE_URI = f"{DRIVER}://{USER}:{PASSWORD}@{HOST}/{BD_HML}"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # permite modificar bd em tempo de execução
    SQLALCHEMY_TRACK_MODIFICATIONS = True
