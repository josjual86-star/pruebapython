from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from models import db, Usuario, Producto, Empleado, Proveedor  
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

    rutas_publicas = [
        "inicio",
        "login",
        "crear_usuario",
        "static"
    ]

    if request.endpoint in rutas_publicas:
        return

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    if "token" not in session:
        session.clear()
        return redirect(url_for("inicio"))

    usuario = Usuario.query.filter_by(
        usuario=session["usuario"],
        activo=True
    ).first()

    if not usuario:
        session.clear()
        return redirect(url_for("inicio"))

    if usuario.token != session["token"]:
        session.clear()
        return redirect(url_for("inicio"))

    if usuario.token_expira is None:
        session.clear()
        return redirect(url_for("inicio"))

    if datetime.now() > usuario.token_expira:
        session.clear()

        usuario.token = None
        usuario.token_expira = None
        db.session.commit()

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

    if usuario_bd:
        print("Usuario encontrado:", usuario_bd.usuario)
    else:
        print("Usuario NO encontrado")

    if usuario_bd and check_password_hash(usuario_bd.password, password):

        print("PASSWORD CORRECTO")

        token = secrets.token_hex(32)

        fecha_expiracion = datetime.now() + timedelta(minutes=1)

        usuario_bd.token = token
        usuario_bd.token_expira = fecha_expiracion

        db.session.commit()

        print("TOKEN GUARDADO:", token)

        session["usuario"] = usuario_bd.usuario
        session["token"] = token

        return redirect(url_for("dashboard"))

    print("PASSWORD INCORRECTO")
    
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
#-------------------------------------------------------------------------------------------------------------------------------------
@app.route("/proveedores")
def proveedores():

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    proveedores = Proveedor.query.filter_by(activo=True).all()

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )

@app.route("/proveedores/nuevo")
def nuevo_proveedor():

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    return render_template("nuevo_proveedor.html")

@app.route("/proveedores/guardar", methods=["POST"])
def guardar_proveedor():

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    empresa = request.form["empresa"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]

    nuevo = Proveedor(
        empresa=empresa,
        telefono=telefono,
        correo=correo
    )

    db.session.add(nuevo)

    db.session.commit()

    return redirect(url_for("proveedores"))

@app.route("/proveedores/editar/<int:id>")
def editar_proveedor(id):

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    proveedor = Proveedor.query.get_or_404(id)

    return render_template(
        "editar_proveedor.html",
        proveedor=proveedor
    )

@app.route("/proveedores/actualizar/<int:id>", methods=["POST"])
def actualizar_proveedor(id):

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    proveedor = Proveedor.query.get_or_404(id)

    proveedor.empresa = request.form["empresa"]
    proveedor.telefono = request.form["telefono"]
    proveedor.correo = request.form["correo"]

    db.session.commit()

    return redirect(url_for("proveedores"))

@app.route("/proveedores/eliminar/<int:id>")
def eliminar_proveedor(id):

    if "usuario" not in session:
        return redirect(url_for("inicio"))

    proveedor = Proveedor.query.get_or_404(id)

    proveedor.activo = False

    db.session.commit()

    return redirect(url_for("proveedores"))