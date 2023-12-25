
from datetime import datetime

class Reservation:
    def __init__(self, reservation_id, user_id, copy_id, start_date, end_date):
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.copy_id = copy_id
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"<Reservation reservation_id={self.reservation_id} user_id={self.user_id} copy_id={self.copy_id} start_date={self.start_date} end_date={self.end_date}>"
