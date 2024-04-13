class JournalEntry:
    def __init__(self, date, rating, notes):
        self.date = date
        self.rating = rating
        self.notes = notes

    def __str__(self):
        return f'{str(self.date)[:-3]} \n\tRating: {str(self.rating)}\n\tNotes:\n{self.notes}'
