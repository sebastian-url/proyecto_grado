from flask_sqlalchemy import SQLAlchemy

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/proyecto"


db = SQLAlchemy()
