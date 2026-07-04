from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    usuario = db.Column(db.String(50), nullable=False)

    password = db.Column(db.String(100), nullable=False)

    activo = db.Column(db.Boolean, default=True)

class Producto(db.Model):

    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    precio = db.Column(db.Numeric(10,2), nullable=False)

    activo = db.Column(db.Boolean, default=True)

class Empleado(db.Model):

    __tablename__ = "empleados"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    puesto = db.Column(db.String(100), nullable=False)

    activo = db.Column(db.Boolean, default=True)