import controller.LibraryController
from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')


library = controller.LibraryController.LibraryController()


@app.before_request
def get_logged_user():
	if '/css' not in request.path and '/js' not in request.path:
		token = request.cookies.get('token')
		time = request.cookies.get('time')
		if token and time:
			request.user = library.get_user_cookies(token, float(time))
			if request.user:
				request.user.token = token


@app.after_request
def add_cookies(response):
	if 'user' in dir(request) and request.user and request.user.token:
		session = request.user.validate_session(request.user.token)
		response.set_cookie('token', session.hash)
		response.set_cookie('time', str(session.time))
	return response


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/catalogue')
def catalogue():
	title = request.values.get("title", "")
	author = request.values.get("author", "")
	page = int(request.values.get("page", 1))
	books, nb_books = library.search_books(title=title, author=author, page=page - 1)
	total_pages = (nb_books // 6) + 1
	return render_template('catalogue.html', books=books, title=title, author=author, current_page=page,
	                       total_pages=total_pages, max=max, min=min)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in dir(request) and request.user and request.user.token:
		return redirect('/')
	email = request.values.get("email", "")
	password = request.values.get("password", "")
	user = library.get_user(email, password)
	if user:
		session = user.new_session()
		resp = redirect("/")
		resp.set_cookie('token', session.hash)
		resp.set_cookie('time', str(session.time))
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = render_template('login.html')
	return resp


@app.route('/logout')
def logout():
	path = request.values.get("path", "/")
	resp = redirect(path)
	resp.delete_cookie('token')
	resp.delete_cookie('time')
	if 'user' in dir(request) and request.user and request.user.token:
		request.user.delete_session(request.user.token)
		request.user = None
	return resp



@app.route('/reserva', methods=['GET'])
def mostrar_pagina_reserva():
    # Renderizar la página de reserva
    return render_template('reserva.html')

@app.route('/reservar', methods=['POST'])
def procesar_reserva():
    # Obtener los datos del formulario
    book_id = request.form['book_id']
    copy_id = request.form['copy_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    # Llamar al método del controlador para añadir la reserva
    resultado = controller.LibraryController.LibraryController.add_reservation(book_id, copy_id, start_date, end_date)

    # Redirigir o mostrar un mensaje según el resultado
    if resultado:
        return redirect(url_for('pagina_exitosa'))  # O mostrar un mensaje de éxito
    else:
        return redirect(url_for('pagina_error'))  # O mostrar un mensaje de error
