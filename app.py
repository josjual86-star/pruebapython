from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from models import db, Usuario, Producto, Empleado
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import timedelta, datetime

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


@app.route("/")
def inicio():
    return render_template("login.html")

@app.route("/crear_usuario", methods=["GET", "POST"])
def crear_usuario():

    if request.method == "POST":

        try:

            usuario = request.form["usuario"]
            password = request.form["password"]
            confirmar = request.form["confirmar_password"]

            if password != confirmar:
                return "Las contraseñas no coinciden"

            existe = Usuario.query.filter_by(usuario=usuario).first()

            if existe:
                return "El usuario ya existe"

            password_hash = generate_password_hash(password)

            nuevo_usuario = Usuario(
                usuario=usuario,
                password=password_hash,
                activo=True
            )

            db.session.add(nuevo_usuario)
            db.session.commit()

            return "Usuario guardado correctamente"

        except Exception as e:
            db.session.rollback()
            return f"ERROR: {e}"

    return render_template("crear_usuario.html")
#------------------------------------------------------------------------------------------------------------------------------------
@app.before_request
def verificar_sesion():

    print("----- BEFORE REQUEST -----")
    print("Endpoint:", request.endpoint)
    print("Session:", session)

    rutas_publicas = [
        "inicio",
        "login",
        "static"
    ]

    if request.endpoint in rutas_publicas:
        return

    if "usuario" not in session:
        print("No hay usuario")
        return redirect(url_for("inicio"))

    if "token" not in session:
        print("No hay token")
        session.clear()
        return redirect(url_for("inicio"))

    print("Hora actual:", datetime.now().timestamp())
    print("Expira:", session.get("expira"))

    if datetime.now().timestamp() > session.get("expira",0):

        print("TOKEN EXPIRADO")

        session.clear()

        return redirect(url_for("inicio"))
    #------------------------------------------------------------------------------------------------------------------------------------

@app.route("/login", methods=["POST"])
def login():

    usuario = request.form["usuario"]
    password = request.form["password"]

    usuario_bd = Usuario.query.filter_by(
        usuario=usuario,
        activo=True
    ).first()

    if usuario_bd and check_password_hash(usuario_bd.password, password):

        session["usuario"] = usuario_bd.usuario

        session["token"] = secrets.token_hex(32)

        session["expira"] = (
            datetime.now() + timedelta(minutes=1)
        ).timestamp()

        return redirect(url_for("dashboard"))

    return render_template(
        "login.html",
        mensaje="Usuario o contraseña incorrectos."
    )

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