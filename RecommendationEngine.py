from User import User
from Book import Book
from Review import Review
from collections import defaultdict

class RecommendationEngine:

    def __init__(self):
        pass


    def recommend_for_user(self, user: User, top_k=10) -> dict[Book: float]:
        raise NotImplementedError


    def recommend_for_book(self, book: Book, top_k=10) -> dict[Book: float]:
        raise NotImplementedError

    def fit(self, data):
        pass

    def update(self, data):
        pass