# Importando app
from app import app

#Flask packages
from flask import flash, redirect, render_template, url_for, request, session

# Models 
from app.models.users import User

# Bcrypt app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Creating routes
@app.route('/')
def index():
    """
    Funcion de vista `Index`
    """
    
    return render_template('auth/index.html')


@app.route('/register/', methods=['POST'])
def register():
    """
    Funcion de vista `Register`
    """

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": request.form['password']
    }

    # Validamos campos
    errores = User.valida_user(data)

    if len(errores) > 0:
        for error in errores:
            print(error)
            flash(error, 'danger')
            
        return redirect('/')

    # Obtenemos un usuario por email
    email = {"email": data['email']}
    user = User.create(email)

    # Consultamos si existe el usuario
    if user:
        flash("El usuario ya existe", "danger")
        return redirect(url_for('index'))
    
    # Consultamos si los passwod hacen match 
    if data['password'] != request.form['confirm_password']:
        flash("Las contraseñas no coinciden", "danger")
        return redirect(url_for('index'))
    
    # Hashing password
    password_hash = bcrypt.generate_password_hash(data['password'])
    data['password'] = password_hash

    # Creating User
    result = User.create(data)

    if result:
        flash("Registro exitoso", "success")
    else:
        flash("Ha ocurrido un error inesperado", "danger")
    
    return redirect(url_for('index'))
    
    
    
    return redirect(url_for('index'))


@app.route('/login/', methods=['POST'])
def login():
    """
    Funcion de vista `Login`
    """

    # Recuperamos los datos del login 
    email = request.form['email']
    password = request.form['password']

    # Consultamos si el email esta registrado
    data = {"email": email}
    user = User.get_by_email(data)

    # Si no esta registrado redirigimos
    if not user:
        flash("El correo no existe", "danger")
        return redirect(url_for('index'))
    
    # Si existe el correo checkeamos el password
    check_password = bcrypt.check_password_hash(user.password, password)
    if check_password:
        session["user"] = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }
        flash("Has iniciado session correctamente", "success")
    else:
        flash("Ha ocurrido un error, vuelva a intentar", "danger")
        return redirect(url_for('index'))
    
    return redirect(url_for('series'))
