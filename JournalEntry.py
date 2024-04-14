class JournalEntry:
    def __init__(self, date, rating, notes, id):
        self.date = date
        self.rating = rating
        self.notes = notes
        self.id = id

    def __str__(self):
        return f'#{self.id}\n\t{str(self.date)[:-3]} \n\tRating: {str(self.rating)}\n\tNotes:\n{self.notes}'
