class Author():
    
    def __init__(self, name, **kwargs):
        self.__name = name
        self.__misc = kwargs
        self.__books = set()

    @property
    def name(self):
        return self.__name
    
    @property
    def misc(self):
        return self.__misc
    
    @property
    def books(self):
        for book in self.__books:
            yield book
    
    def add_book(self, book):
        self.__books.add(book) #use add

    def delete_book(self, book):
        self.__books.discard(book) #or use remove？

    @property
    def rating(self):
        return sum([book.rating for book in self.__books])/len(self.__books)
