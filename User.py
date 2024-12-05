from Review import Review



""" in the user part. for user newly come, should we assigned a new user id in the form of dataset or creat our new id? 
    I prefferr to create our new id. and stored in a new csv file locally.
"""



class User:
    def __init__(self, user_id, name, **kwargs):
        self.__user_id = user_id
        self.__info = kwargs
        self.__name = name
        self.__reviews = dict()
        

    @property
    def user_id(self):
        return self.__user_id
    
    @property
    def name(self):
        return self.__name
    
    def __hash__(self) -> int:
        return hash(self.__user_id)

    
    @property
    def info(self):
        return {**self.__info}
    
    @property
    def reviews(self):

        return {book: review for book, review in self.__reviews.items()}

    def delete_review(self, book):
        if book in self.__reviews:
            del self.__reviews[book]

    def add_review(self, review, update=False):
        # make sure not previous review has been done on a same book
        if not hasattr(review, "isbn"):
            raise AttributeError("The review object must have a 'isbn' attribute.")

        if review.isbn in self.__reviews and not update:
            raise Exception(f"Duplicate review for book: {review.isbn} for user: {self.user_id}")

        self.__reviews[review.isbn] = review


    def edit_review(self, review):
        # check if review exists
        if not hasattr(review, "book"):
            raise AttributeError("The review object must have a 'book' attribute.")

        if review.book not in self.__reviews:
            raise Exception(f"Review not found for book: {review.book}")

        self.__reviews[review.book] = review