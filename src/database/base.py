
from sqlalchemy.orm import Mapped, declarative_base
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()
db = SQLAlchemy(model_class=Base, engine_options=dict(echo=True))