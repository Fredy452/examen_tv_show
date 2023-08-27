# Importando app
from app import app

# flask
from flask import redirect, render_template, session, request, flash, url_for


# Import Model 
from app.models.series import Serie

# Creating routes for dashboard
@app.route('/series/')
def series():
    """
    Funcion de vista `dashboard`
    """
    # Protegiendo ruta
    if not session.get("user"):
        return redirect('/')
    
    # Obtenemos todas las series
    series = Serie.get_serie_whit_user()
    # for serie in series:
    #     print(serie)

    
    return render_template('series/index.html', series=series)

@app.route('/logout/')
def logout():
    """
    Funcion de vista cerrar sesion
    """
    session.clear()

    return redirect('/')

@app.route('/series/new/')
def series_new():
    """
    Funcion de vista series new
    """
    if not session.get("user"):
        return redirect('/')

    return render_template('series/create.html')

@app.route('/series/create/', methods=['POST'])
def series_create():
    """
    Funcion de vista crear series
    """
    if not session.get("user"):
        return redirect('/')
    # Generamos dictionary
    data = {
        "user_id": session["user"]["id"],
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['release_date'],
        "description": request.form['description']
    }

    # Enviamos data para validar 
    errors = Serie.validar_serie(data)

    if len(errors) > 0:
        for error in errors:
            print(error)
            flash(error, 'danger')
            
        return redirect(url_for('series_new'))

    # Si no hay eror creamos el objeto
    serie = Serie.create(data)

    # Manejando exepciones
    if serie:
        flash("serie creada con exito", "success")
    else:
        flash("Ha ocurrido algun error", "danger")

    return redirect(url_for('series'))

# Creamos una ruta mostrar series
@app.route('/serie/<int:id>/')
def serie_show(id):
    """
    Funcion de vista mostrar
    """
    if not session.get("user"):
        return redirect('/')
    # Obtenemos la serie que recibimos por id
    data = {
        "id": id
    }
    serie = Serie.get_one(data)
    print(serie)
    
    return render_template("series/show.html", serie=serie)


# Creamos una ruta editar series
@app.route('/serie/edit/<int:id>/')
def serie_edit(id):
    """
    Funcion de vista mostrar
    """
    if not session.get("user"):
        return redirect('/')
    # Obtenemos la serie que recibimos por id
    data = {
        "id": id
    }
    serie = Serie.get_one(data)
    

    return render_template("series/edit.html", serie=serie)

@app.route('/serie/edit_proccess/<int:id>/', methods=['POST'])
def serie_edit_proccess(id):
    """
    Funcion de vista editar
    """
    if not session.get("user"):
        return redirect('/')
    # Generamos dictionary
    data = {
        "id": id,
        "user_id": session["user"]["id"],
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['release_date'],
        "description": request.form['description'],
    }
    # Primero validamos
    errors = Serie.validar_serie(data)
    if len(errors) > 0:
        for error in errors:
            print(error)
            flash(error, 'danger')
    

    # Si no hay eror creamos el objeto
    Serie.update(data)
    flash("serie editada con exito", "success")


    return redirect(url_for('series'))

@app.route('/serie/delete/<int:id>')
def serie_delete(id):
    """
    Funcion de viata para eliminar serie
    """
    
    data = {
        "id": id
    }
    series = Serie.get_serie_whit_user()
    for serie in series:
        # Solo el usuario que creó la serie puede eliminarla
        if session["user"]["id"] == serie["user_id"]:
            flash("La serie fue eliminada", "success")
            Serie.delete(data)
            return redirect(url_for("series"))
    
    flash("No tienes permiso para eliminar la serie", "danger")

    return redirect(url_for('series'))

# @app.route('/serie/like/<int:user_id>/<int:serie_id>')
# def serie_like(user_id, serie_id):
#     """
#     Funcion para dar like
#     """
    
#     data = {
#         "user_id": user_id,
#         "serie_id": serie_id
#     }
#     Serie.like(data)


#     return redirect(url_for('series'))

# @app.route('/serie/unlike/<int:user_id>/<int:serie_id>')
# def serie_unlike(user_id, serie_id):

#     return redirect(url_for('series'))

