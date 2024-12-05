from Review import Review
from User import User
from Book import Book
from tqdm import tqdm
from VectorRecommendationEngine import VectorRecommendationEngine

import os
import pickle

"top 10 books: authors, date, genre, rating, reviews"

"which one u want to read?"

"reviews and rating of the book" 

"after puchasing or read: review and rating the book"

"first rating, then review"

"rating: 1-5"

"review limited 100 words"

"after reivew: upload the recommnandation book base on current book"

"""recommandation: if user do not like it which rating below 3, then recommand any other book not in the same set
                2. if user like it which rating above 3, then recommand any other book in the same set
                3. as user rates more, the recommandation will be more accurate which recommand the same catogory books
                """
                

class ApplicationInterface():
    
    def __init__(self):
        self.__users : dict[str, User] = {}
        self.__books : dict[str, Book] = {}
        self.__reviews : dict[tuple[str, str], Review] = {}
        self.__indexed = False

        self.recommendation_engine = VectorRecommendationEngine()
    
    @property
    def users(self):
        for user in self.__users.values():
            yield user

    @property
    def books(self):
        for book in self.__books.items():
            yield book

    @property
    def reviews(self):
        for review in self.__reviews.values():
            yield review
            
    def delete_review(self, user_id: str, isbn: str):
        del self.__reviews[(user_id, isbn)]
        self.get_user(user_id).delete_review(isbn)
        self.get_book(isbn).delete_review(user_id)

    def get_user(self, user_id: str):
        return self.__users.get(user_id, None)
    
    def get_book(self, isbn: str):
        return self.__books.get(isbn, None)
    
    def get_review(self, user_id: str, isbn: str):
        return self.__reviews.get((user_id, isbn), None)

    def add_review(self, review: Review, update=False):
        if (review.user_id, review.isbn) in self.__reviews and not update:
            #  review from user to book already exists
            raise Exception(f"Review from user {review.user_id} to book {review.isbn} already exists.")
        self.__reviews[(review.user_id, review.isbn)] = review
        
        # sync user and book
        user=self.get_user(review.user_id)
        book=self.get_book(review.isbn)

        # assert user is not None and book is not None
        # we shouldn't allow review from a non existing user or to a non existing book

        user.add_review(review, update=update)
        book.add_review(review, update=update)

    def add_user(self, user: User):

        if user.user_id in self.__users:
            raise Exception(f"User {user.user_id} already exists.")

        self.__users[user.user_id] = user
        return user
    
    def add_book(self, book: Book, update=False):

        if book.isbn in self.__books: 
            raise Exception(f"Book {book.isbn} already exists.")
        
        self.__books[book.isbn] = book
        
        # modify the recommendation engine
        if self.recommendation_engine and update:
            self.recommendation_engine.udpate(book)
        
        
        return book
    
    def index(self, batch_size=256):

        data = self.__books.values()
        keys = [book.isbn for book in data]
        book_list = [book.representation() for book in data]

        # return book_list

        if self.recommendation_engine:
            self.recommendation_engine.fit(data=self.__books.values(), batch_size=batch_size)
            self.__indexed = True
    
    def recommend_by_user(self, user_id):
        # todo: user based and book based recommendation
        if not self.__indexed:
            raise Exception("Indexing not done yet.")
        
        return self.recommendation_engine.recommend_for_user(self.get_user(user_id))
    
    def recommend_by_book(self, book_id):
        # todo: user based and book based recommendation
        if not self.__indexed:
            raise Exception("Indexing not done yet.")
        
        return self.recommendation_engine.recommend_for_book(self.get_book(book_id))
    
    
    def search_title(self, title):
        results = []
        for book in self.__books.values():
            if title.lower() in book.title.lower():
                results.append(book)
        return results
    
    def search_author(self, author):
        results = []
        for book in self.__books.values():
            if author.lower() in author.title.lower():
                results.append(book)
        return results
    
    def search_isbn(self, isbn):
        results = []
        for book in self.__books.values():
            if isbn.lower() in book.isbn.lower():
                results.append(book)
        return results
    
    def search_genre(self, genre):
        results = []
        for book in self.__books.values():
            if genre.lower() in book.genre.lower():
                results.append(book)
        return results
    
    def search_similar_book(self, other: Book):
        pass
    
    def book_summary(self, book: Book):
        pass
    
    
    def user_summary(self, user: User):
        pass
    
    def load_from_dataset(self, books_path = './dataset/books_data.csv', reviews_path = './dataset/Books_rating.csv'):
        import pandas as pd
        import numpy as np
        print("Loading data from dataset 0/2 done...")
        books_data = pd.read_csv('./dataset/books_data.csv').dropna(axis=0)
        n_books = len(books_data)
        print(f'1/2 done, {n_books} books loaded...')
        reviews_data = pd.read_csv('./dataset/Books_rating.csv').dropna(axis=0)
        n_reviews = len(reviews_data)
        print(f'2/2 done, {n_reviews} reviews loaded...')

        for _, row in tqdm(books_data.iterrows(), total=n_books, desc="Loading books data..."):
            book = Book(row.Title, row.authors, row.description, row.publishedDate, genre=row.categories)
            self.add_book(book)
        print(len(self.__books))

        error_count = 0

        for _, row in tqdm(reviews_data.iterrows(), total=n_reviews, desc="Loading reviews data..."):
            
            if (user := self.get_user(row.User_id)) is None:
                user = User(row.User_id, name=row.profileName)
                self.add_user(user)
            book = self.get_book(row.Title)
            review = Review(user_rsp=row.profileName, isbn=row.Title, user_id=row.User_id, usr_rating=int(row['review/score']), review=row['review/text'])

            if book is None or user is None:
                # print(f'user {row.User_id} or book {row.Id} not found in dataset')
                continue

            try:
                self.add_review(review)
            except Exception as e:
                error_count += 1
                continue
                
        print(f'{error_count} errors occurred during data loading')

    
    @staticmethod
    def auto_load(force=False, source='./application.pkl'):
        if os.path.exists(source) and not force:
            print(f'Loading application from {source}...')
            with open(source, 'rb') as f:
                return pickle.load(f)
        else:
            app = ApplicationInterface()
            app.load_from_dataset()
            with open(source, 'wb') as f:
                pickle.dump(app, f)
            return app
        
    def save_state(self, source='./application.pkl'):
        with open(source, 'wb') as f:
            pickle.dump(self, f)


    def __del__(self):
        # with open('./application.pkl', 'wb') as f:
        #     pickle.dump(self, f)
        pass


    
    def register(self):
        pass
    

    def login(self):
        pass


