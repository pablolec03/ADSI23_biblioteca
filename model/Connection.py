import sqlite3

class Connection:
	def __init__(self):
		self.con = sqlite3.connect("datos.db", check_same_thread=False)
		self.cur = self.con.cursor()

	def select(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		rows = self.cur.fetchall()
		return [x for x in rows]

	def insert(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		self.con.commit()
		answ = self.cur.rowcount
		return answ

	def update(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		self.con.commit()

	def delete(self, sentence, parameters=None):
		if parameters:
			self.cur.execute(sentence, parameters)
		else:
			self.cur.execute(sentence)
		answ = self.cur.rowcount
		self.con.commit()
		return answ

db = Connection()