import sqlalchemy

from db.postgres import Base


class Template(Base):
    __tablename__ = 'templates'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    event = sqlalchemy.Column(sqlalchemy.String(30), unique=True, index=True)
    is_instant = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    title = sqlalchemy.Column(sqlalchemy.String(30))
    text = sqlalchemy.Column(sqlalchemy.Text)
