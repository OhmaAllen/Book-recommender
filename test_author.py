import pytest
from Author import Author
from Book import Book
from Review import Review
from datetime import date

@pytest.fixture
def dummy_author():
    return Author(name="John Doe", genre="Fiction")

@pytest.fixture
def dummy_book():
    return Book(title="Test Book", author="John Doe", desc="A test description", pub_date=date(2020, 1, 1))

@pytest.fixture
def dummy_review():
    return Review(user_rsp="Test User", isbn="1234567890", user_id=1, usr_rating=4, review="Great book!")

def test_author_initialization(dummy_author):
    assert dummy_author.name == "John Doe"
    assert dummy_author.misc == {"genre": "Fiction"}
    assert list(dummy_author.books) == []

def test_author_add_book(dummy_author, dummy_book):
    dummy_author.add_book(dummy_book)
    assert len(list(dummy_author.books)) == 1

def test_author_delete_book(dummy_author, dummy_book):
    dummy_author.add_book(dummy_book)
    dummy_author.delete_book(dummy_book)
    assert len(list(dummy_author.books)) == 0

def test_author_rating(dummy_author, dummy_book, dummy_review):
    dummy_book.add_review(dummy_review)
    dummy_author.add_book(dummy_book)
    assert dummy_author.rating == 4
