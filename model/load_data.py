import sqlite3
import json

import pandas as pd
import requests

all_sheets = pd.read_excel('ListadoLibros.xls', sheet_name=None)

import hashlib
salt = "library"

with open('db-libros.json','r') as f:
	libros = json.load(f)

print(len(libros["usuarios"]))


con = sqlite3.connect("datos.db")
cur = con.cursor()

if False:
	cur.execute("""
	CREATE TABLE Author(
		id integer primary key AUTOINCREMENT,
		name varchar(40)
	)
	""")

	cur.execute("""
	CREATE TABLE Book(
		id integer primary key AUTOINCREMENT,
		title varchar(50),
		author integer,
		cover varchar(50),
		description TEXT,
		FOREIGN KEY(author) REFERENCES Author(id)
	)
	""")

	cur.execute("""
	CREATE TABLE User(
		id integer primary key AUTOINCREMENT,
		name varchar(20),
		email varchar(30),
		password varchar(32)
	)
	""")

	cur.execute("""
	CREATE TABLE Session(
		session_hash varchar(32) primary key,
		user_id integer,
		last_login integer,
		FOREIGN KEY(user_id) REFERENCES User(id)
	)
	""")

	for user in libros['usuarios']:
		dataBase_password = user['password'] + salt
		hashed = hashlib.md5(dataBase_password.encode())
		dataBase_password = hashed.hexdigest()
		cur.execute(f"""INSERT INTO User VALUES (NULL, '{user['nombres']}', '{user['email']}', '{dataBase_password}')""")


for key, df in all_sheets.items():
	num = len(df[list(df.keys())[0]])
	if key < 'D':
		continue
	for i,book in enumerate(zip(*[df[x] for x in df.keys()[:4]])):
		if key == 'D' and i < 0:
			continue
		print(f"\r{key} -- {i} / {num}     ", end="")
		resp = requests.get(url="https://openlibrary.org/search.json?title="+'+'.join(book[2].split()))
		data = resp.json()
		if data['num_found'] > 0:
			b = data['docs'][0]
			title = b['title']
			try:
				author = b["author_name"][0]
			except:
				author = str(book[1]) + ' ' + str(book[0])
			if 'cover_i' in b:
				icon = f"https://covers.openlibrary.org/b/id/{b['cover_i']}-L.jpg"
			else:
				icon = None
			try:
				resp = requests.get(url=f"https://openlibrary.org/api/books?bibkeys=ISBN:{b['isbn'][0]}&format=json&jscmd=details")
				data = resp.json()
				data = data[list(data.keys())[0]]
			except:
				data = {'details': {}}
			try:
				if 'excerpts' in data['details']:
					description = data['details']['excerpts']['value']
				elif "description" in data['details']:
					description = data['details']["description"]['value']
				else:
					description = None
			except:
				description= None
		else:
			title = book[2]
			author = str(book[1]) + ' ' + str(book[0])
			icon = None
			description = None

		cur.execute(f"""INSERT INTO Author VALUES (NULL, '{author}')""")
		res = cur.execute(f"SELECT id FROM Author WHERE name='{author}'")
		author_id = res.fetchone()[0]

		cur.execute("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?)",
		            (title, author_id, icon, description))
		con.commit()
	print()



