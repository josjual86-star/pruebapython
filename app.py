from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from models import db, Usuario, Producto, Empleado

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


@app.route("/")
def inicio():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():

    usuario = request.form["usuario"]
    password = request.form["password"]

    usuario_bd = Usuario.query.filter_by(
        usuario=usuario,
        password=password,
        activo=True
    ).first()

    if usuario_bd:

        session["usuario"] = usuario_bd.usuario

        return redirect(url_for("dashboard"))

    else:

        return "Usuario o contraseña incorrectos"

@app.route("/dashboard")
def dashboard():

    if "usuario" not in session:

        return redirect(url_for("inicio"))

    return render_template(
        "dashboard.html",
        usuario=session["usuario"]
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("inicio"))

@app.route("/productos")
def productos():

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    productos = Producto.query.filter_by(activo=True).all()

    return render_template(
        "productos.html",
        productos=productos
    )

@app.route("/empleados")
def empleados():

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    empleados = Empleado.query.filter_by(activo=True).all()

    return render_template(
        "empleados.html",
        empleados=empleados
    )

@app.route("/productos/nuevo")
def nuevo_producto():

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    return render_template("nuevo_producto.html")

@app.route("/productos/guardar", methods=["POST"])
def guardar_producto():

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    nombre = request.form["nombre"]
    precio = request.form["precio"]

    nuevo = Producto(
        nombre=nombre,
        precio=precio
    )

    db.session.add(nuevo)

    db.session.commit()

    return redirect(url_for("productos"))

@app.route("/productos/editar/<int:id>")
def editar_producto(id):

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    producto = Producto.query.get_or_404(id)

    return render_template(
        "editar_producto.html",
        producto=producto
    )

@app.route("/productos/actualizar/<int:id>", methods=["POST"])
def actualizar_producto(id):

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    producto = Producto.query.get_or_404(id)

    producto.nombre = request.form["nombre"]

    producto.precio = request.form["precio"]

    db.session.commit()

    return redirect(url_for("productos"))

@app.route("/productos/eliminar/<int:id>")
def eliminar_producto(id):

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    producto = Producto.query.get_or_404(id)

    producto.activo = False

    db.session.commit()

    return redirect(url_for("productos"))

@app.route("/empleados/guardar", methods=["POST"])
def guardar_empleado():

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    nuevo = Empleado(

        nombre=request.form["nombre"],

        puesto=request.form["puesto"]

    )

    db.session.add(nuevo)

    db.session.commit()

    return redirect(url_for("empleados"))

@app.route("/empleados/editar/<int:id>")
def editar_empleado(id):

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    empleado = Empleado.query.get_or_404(id)

    return render_template(
        "editar_empleado.html",
        empleado=empleado
    )

@app.route("/empleados/actualizar/<int:id>", methods=["POST"])
def actualizar_empleado(id):

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    empleado = Empleado.query.get_or_404(id)

    empleado.nombre = request.form["nombre"]

    empleado.puesto = request.form["puesto"]

    db.session.commit()

    return redirect(url_for("empleados"))

@app.route("/empleados/eliminar/<int:id>")
def eliminar_empleado(id):

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    empleado = Empleado.query.get_or_404(id)

    empleado.activo = False

    db.session.commit()

    return redirect(url_for("empleados"))

@app.route("/empleados/nuevo")
def nuevo_empleado():

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    return render_template("nuevo_empleado.html")

if __name__ == "__main__":
    app.run(debug=True)