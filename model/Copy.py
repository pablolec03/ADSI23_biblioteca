
class Copy:
    def __init__(self, copy_id, book_id, status='available'):
        self.copy_id = copy_id
        self.book_id = book_id
        self.status = status  # Possible statuses: 'available', 'reserved', 'checked_out'

    def __repr__(self):
        return f"<Copy copy_id={self.copy_id} book_id={self.book_id} status={self.status}>"
