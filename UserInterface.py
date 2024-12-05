from ApplicationInterface import ApplicationInterface
from Book import Book
from User import User
from Review import Review
import os
from VectorRecommendationEngine import VectorRecommendationEngine
import time

# decorator
from functools import wraps
from argparse import ArgumentParser


def login_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.logged_in():
            return self.not_logged_in
            
        return func(self, *args, **kwargs)
    return wrapper

def clear_before(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        time.sleep(1)
        os.system('clear' if os.name == 'posix' else 'cls')
        return func(self, *args, **kwargs)
    return wrapper

def instack(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.push(func, *args, **kwargs)
        return func(self, *args, **kwargs)
    return wrapper

def flush_stack(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.__stack = []
        return func(self, *args, **kwargs)
    return wrapper

class UserInterface:
    def __init__(self, source='./application.pkl', force=False, auto_login=None):
        self.__app = ApplicationInterface.auto_load(force=force, source=source)
        self.__user = None
        self.__book = None
        self.__review = None
        self.__stack = []

        self.__auto_login = auto_login
    
    def push(self, func, *args, **kwargs):
        self.__stack.append((func, args, kwargs))

    def logged_in(self):
        return self.__user is not None
    
    
    def back(self):
        if not self.__stack: self.menu()
        else:
            top = self.__stack.pop()
            top[0](self, *top[1], **top[2])

    @flush_stack
    @clear_before
    def menu(self):
        if self.logged_in(): print(f'Logged in as {self.__user.user_id}')
        print("\n----Main Menu----")
        print("1) Login")
        print("2) Register")

        # search book
        print("3) Search Book")
        # user summary
        print("4) User Summary")
        # recommendation
        print("5) Recommendation")
        # review
        print("E) Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            self.login()
        elif choice == "2":
            self.register()
        elif choice == "3":
            self.search_book()
        elif choice == "4":
            self.user()
        elif choice == "5":
            self.recommendation()
        elif choice == "E":
            self.confirm_exit()
        else:
            print("Invalid choice.")
            self.menu()



    
    @clear_before
    def not_logged_in(self):
        print("You are not logged in. Please 1) login or 2) register.")
        print("3) menu.")

        choice = input("Enter your choice: ")

        if choice == "1":
            self.login()
        elif choice == "2":
            self.register()
        elif choice == "3":
            self.menu()
        else:
            print("Invalid choice.")
            self.not_logged_in()

    @clear_before
    def confirm_exit(self):
        print("Are you sure you want to exit? (y/n)")
        if input() == "y":
            self.exit()
        else:
            self.menu()

    @clear_before
    def exit(self):
        print("Goodbye!")
        exit()

    @clear_before
    def login(self):
        print(f"Please enter your username:", end=" ")
        user_id = input()
        if self.__app.get_user(user_id) is None:
            print(f"User {user_id} does not exist.")
            self.return_main()
        self.__user = self.__app.get_user(user_id)
        self.back()
        
    @clear_before
    def register(self):
        user_id = input(f"Please enter your User Id: ")
        name = input(f"Please enter your Name:")
        try:
            self.__app.add_user(User(user_id, name))
        except Exception as e:
            print(e)
            print(f"User {user_id} already exists, logging in...")
        self.__user = self.__app.get_user(user_id)
        self.back()

    


    @login_required
    @clear_before
    @instack
    def user(self):
        print("----User----")
        print(f" {'User':<15}{self.__user.name}")
        for info, content in self.__user.info.items():
            print(f" {info:<15}{content}")
        print("1) Reviews")
        print("E) Back to Main Menu")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            reviews = self.__user.reviews.values()
            self.view_reviews(reviews)  
        elif choice == "E":
            self.back()
        else:
            print("Invalid choice.")
            input('Press any key to go back to user...')
            self.user()


    @login_required
    @clear_before
    def view_recommendation(self, recommendations):
        print("----Recommendations----")
        if not recommendations:
            print("No recommendations available.")
        else:
            for idx, rec in enumerate(recommendations, start=1):
                print(f"{idx}. {rec}")  
        print("\nE) Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "E":
            self.menu()
        else:
            print("Invalid choice.")
            self.view_recommendation(recommendations)


    @login_required
    def recommendation(self):   
        print ("----Recommendation----")

        if not self.__app._ApplicationInterface__indexed:
            print("Indexing the data, please wait...")
            self.__app.index()

        print("1) Recommend for Current User")
        print("E) Back to Main Menu")
        # print("2) Recommend for Book")


        choice = input("Enter your choice: ")
        r_to_user = self.__app.recommend_by_user(self.__user.user_id)
        # r_to_book = self.__app.recommend_by_book(self.__book.isbn)

        if choice == "1":
            self.view_recommendation(r_to_user)
        # if choice == "2":
        #     print(f"Recommendation for Book {self.__book.title}")



    @flush_stack
    @instack
    def book(self):
        print("----Book----")
        print("1) View Reviews")
        print("2) Add Review")
        print("E) Back to Main Menu")
        
        # get user choice
        
        choice = input("Enter your choice: ")
        if choice == "1":
            self.view_reviews(self.__book.reviews)
        elif choice == "2":
            self.add_review()
        elif choice == "E":
            self.back()
        else:
            print("Invalid choice.")
            input('Press any key to go back to book review...')
            self.book_review()
            
    @login_required
    @clear_before
    def add_review(self):
        print("----Add Review----")
        if not self.__book:
            print("You haven't specified a book to add a review.")
            self.return_main()
        else:
            print(f"----Add Review for Book {self.__book.title}----")
            while 1:
                rating = input("Enter rating (1-5): ")
                try:
                    assert 1 <= int(rating) <= 5
                    break
                except:
                    print("Invalid rating.")
            rating = float(rating)
            while 1:
                review = input("Enter review: ")
                if not review:
                    print("Review cannot be empty.")
                else:
                    break
            self.__app.add_review(Review(self.__user.info.get('name', self.__user.user_id), self.__book.isbn, self.__user.user_id, rating, review))
            print("Review added successfully.")
            self.back()
        
    @clear_before
    @instack
    def view_reviews(self, reviews):
        review_list = list(reviews)
        
        def preview_review(review: Review):
            return f"{review.user_id:<15}{review.usr_rating}"
        
        for i, review in enumerate(review_list):
            if isinstance(review, tuple):
                review = review[1]
            print(f"{i+1}). {preview_review(review)}")
        
        print("E) Back to Main Menu")
        # user choice
        
        choice = input("Enter your choice: ")
        if choice == "E":
            self.back()
        else:
            if choice.isdigit(): 
                choice = int(choice)
                if 1 <= choice <= len(review_list):
                    self.__review = review_list[choice-1]
                    self.review()
                    return
            print("Invalid choice.")
            
            
    @flush_stack
    @clear_before
    def return_main(self):
        input('Press any key to go back to main menu...')
        self.menu()
    
        
        
    @clear_before
    @instack
    def review(self):
        print("----Review----")
        print('User: ', self.__review.user_rsp)
        print('Rating: ', self.__review.usr_rating)
        print('Review: ', self.__review.review)
        
        print("1) Modify Review")
        print("2) Delete Review")
        print("E) Back to Main Menu")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            self.modify_review()
        elif choice == "2":
            self.delete_review()
        elif choice == "E":
            self.back()
        else:
            print("Invalid choice.")
            self.review()
            
    @login_required
    @clear_before
    def modify_review(self):
              
        if not self.__review or not self.__user:
            print("You havn't specified a review to modify.")
            self.return_main()
        elif self.__review.user_id != self.__user.user_id:
            print("You are not authorized to modify this review.")
            self.return_main()
            
        else:
            print("----Modify Review----")
            print(f'Review for Book {self.__review.isbn}')
            while 1:
                rating = input("Enter rating (1-5): ")
                try:
                    assert 1 <= int(rating) <= 5
                    break
                except:
                    print("Invalid rating.")
            rating = float(rating)
            while 1:
                review = input("Enter review: ")
                if not review:
                    print("Review cannot be empty.")
                else:
                    break
            self.__app.add_review(Review(self.__user.info.get('name', self.__user.user_id), self.__review.isbn, self.__user.user_id, rating, review), update=True)
            print("Review modified successfully.")
            self.back()
                
            

    @login_required
    @clear_before
    def delete_review(self):
        try:
            self.__app.delete_review(self.__review.user_id, self.__review.isbn)
            print('deletion successful')
        except Exception as e:
            print(e)
        self.back()
        
    


    def run(self):
        if self.__auto_login:
            self.__user = self.__app.get_user(self.__auto_login)
        while True: self.menu() 

    @login_required
    @clear_before
    def view_recommendation(self, recommendations):
        print("----Recommendations----")
        if not recommendations:
            print("No recommendations available.")
        else:
            for idx, rec in enumerate(recommendations, start=1):
                print(f"{idx}. {rec}")  
        print("\nE) Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "E":
            self.back()
        else:
            print("Invalid choice.")
            self.view_recommendation(recommendations)



    "return a book list all navigateto the booklist"

    "recommand return a booklist, search reccomand for book and user"


    @login_required
    def recommendation(self):   
        print ("----Recommendation----")
        print("1) Recommend for User")
        # print("2) Recommend for Book")
        if not self.__app._ApplicationInterface__indexed:
            print("Indexing the data, please wait...")
            self.__app.index()

        choice = input("Enter your choice: ")
        r_to_user = self.__app.recommend_by_user(self.__user.user_id)
        # r_to_book = self.__app.recommend_by_book(self.__book.isbn)
        if choice == "1":
            self.book_list(r_to_user)
        # if choice == "2":
        #     print(f"Recommendation for Book {self.__book.title}")

    @clear_before
    def search_book(self):
        print("----Search Book----")
        print("1) Search by Title")
        print("2) Search by Author")
        print("3) Search by Genre")
        print("E) Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter the book title to search: ")
            results = self.__app.search_title(title)
            self.book_list(results)
        elif choice == "2":
            author = input("Enter the author's name to search: ")
            results = self.__app.search_author(author)
            self.book_list(results)
        elif choice == "3":
            genre = input("Enter the genre to search: ")
            results = self.__app.search_genre(genre)
            self.book_list(results)
        elif choice == "E":
            self.menu()
        else:
            print("Invalid choice.")
            self.search_book()

    
    @clear_before
    @instack
    def book_list(self, books, max_books=10):
        if not books:
            print("No books found.")
            self.return_main()
        else:
            print("----Book List----")
            for idx, book in enumerate(books, start=1, maxlen=max_books):
                print(f"{idx}. {book.title} by {book.author} (Genre: {book.genre}, ISBN: {book.isbn})")
            
            print("\nE) Back to Main Menu")
            choice = input("Enter your choice: ")
            if choice == "E":
                self.menu()
            elif choice.isdigit() and 1 <= int(choice) <= len(books):
                self.__book = books[int(choice) - 1]
                self.book()
            else:
                print("Invalid choice.")
                self.book_list(books)


    @clear_before
    @instack
    def book(self):
        print("----Book----")

        print(f" {'Title':<15}{self.__book.title}")
        print(f" {'Author':<15}{self.__book.author}")
        print(f" {'Genre':<15}{self.__book.genre}")
        print(f" {'Rating':<15}{self.__book.rating}")
        print(f" {'Description':<15}{self.__book.desc}")

        print("1) Add Review")
        print("2) View Reviews")
        print("3) Similar Books")
        print("E) Back to Main Menu")

        choice = input("Enter your choice: ")
        if choice == "1":
            self.add_review()
        elif choice == "2":
            reviews = self.__book.display_reviews()
            self.view_reviews(reviews)
        elif choice == "3":
            similar_books = self.__app.recommend_by_book(self.__book.isbn)
            self.book_list(similar_books)
        elif choice == "E":
            self.back()
        else:
            print("Invalid choice.")
            self.book()