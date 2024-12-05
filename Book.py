from datetime import date
from Review import Review

class Book:

    def __init__(self, title, author, desc, pub_date,  isbn=None, **kwargs):
        self.__title = title
        self.__author = author
        self.__desc = desc
        self.__pub_date = pub_date
        # self.__isbn = isbn
        if isbn is not None:
            self.__isbn = isbn
        else:
            self.__isbn = title
        self.__reviews = {}

        self.__genre = kwargs.get('genre', 'unknown')

    @property
    def title(self):
        return self.__title
    
    @property
    def genre(self):
        return self.__genre
    
    @property
    def author(self):
        return self.__author
    
    @property
    def desc(self):
        return self.__desc
    
    @property
    def pub_date(self):
        return self.__pub_date
    
    @property
    def isbn(self):
        ##!! Note that the dataset doesn't provide the isbn by default, we need to find some other way to uniquely identify a book


        ## i belive book have id as unique number 
        return self.__isbn

    @property
    def rating(self):
        if not self.__reviews:
            return None
        return sum([review.usr_rating for review in self.__reviews.values()]) / len(self.__reviews)

    
    def add_review(self, review, update=False):
        if not isinstance(review, Review):
            raise TypeError("Expected a Review object.")
        if not update and review.user_id in self.__reviews:
            raise Exception(f"Review from user {review.user_id} already exists.")
        self.__reviews[review.user_id] = review
        
    def delete_review(self, user_id):
        if user_id in self.__reviews:
            del self.__reviews[user_id]


    def display_reviews(self):
        for review in self.__reviews.items():
            yield review

    def __hash__(self) -> int:
        return hash(self.__isbn)

    def representation(self):
        return f"Title: {self.title} Genre: {self.genre} Description: {self.desc}"
    