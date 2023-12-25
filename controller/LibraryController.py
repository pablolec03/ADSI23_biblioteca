from model import Connection, Book, User
from model.tools import hash_password

db = Connection()

class LibraryController:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(LibraryController, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance


    def search_books(self, title="", author="", limit=6, page=0):
        count = db.select("""
                SELECT count() 
                FROM Book b, Author a 
                WHERE b.author=a.id 
                    AND b.title LIKE ? 
                    AND a.name LIKE ? 
        """, (f"%{title}%", f"%{author}%"))[0][0]
        res = db.select("""
                SELECT b.* 
                FROM Book b, Author a 
                WHERE b.author=a.id 
                    AND b.title LIKE ? 
                    AND a.name LIKE ? 
                LIMIT ? OFFSET ?
        """, (f"%{title}%", f"%{author}%", limit, limit*page))
        books = [
            Book(b[0],b[1],b[2],b[3],b[4])
            for b in res
        ]
        return books, count

    def get_user(self, email, password):
        user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2])
        else:
            return None

    def get_user_cookies(self, token, time):
        user = db.select("SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?", (time, token))
        if len(user) > 0:
            return User(user[0][0], user[0][1], user[0][2])
        else:
            return None


    def add_reservation(self, user_id, copy_id, start_date, end_date):
        # Verificar si la copia está disponible
        if not self.check_copy_availability(copy_id, start_date, end_date):
            return False  # La copia no está disponible

        # Añadir la reserva en la base de datos
        insert_query = "INSERT INTO Reservations (user_id, copy_id, start_date, end_date) VALUES (?, ?, ?, ?)"
        db.execute(insert_query, (user_id, copy_id, start_date, end_date))
        db.commit()
        return True


    def check_copy_availability(self, copy_id, start_date, end_date):
        # Comprobar si hay reservas existentes que se solapen con las fechas dadas
        check_query = "SELECT * FROM Reservations WHERE copy_id = ? AND (start_date BETWEEN ? AND ? OR end_date BETWEEN ? AND ?)"
        db.execute(check_query, (copy_id, start_date, end_date, start_date, end_date))
        reservations = db.fetchall()
        return len(reservations) == 0  # Retorna True si no hay reservas que se solapen


    def get_user_reservations(self, user_id):
        # Obtener todas las reservas del usuario
        query = "SELECT * FROM Reservations WHERE user_id = ?"
        db.execute(query, (user_id,))
        return db.fetchall()

