import pytest
from datetime import date
from Book import Book
from Review import Review

@pytest.fixture
def dummy_book():
    return Book(title="Test Book", author="John Doe", desc="A test description", pub_date=date(2020, 1, 1))

@pytest.fixture
def dummy_review():
    return Review(user_rsp="Test User", isbn="1234567890", user_id=1, usr_rating=4, review="Great book!")

def test_book_initialization(dummy_book):
    assert dummy_book.title == "Test Book"
    assert dummy_book.author == "John Doe"
    assert dummy_book.desc == "A test description"
    assert dummy_book.pub_date == date(2020, 1, 1)
    assert dummy_book.isbn == "Test Book"  

def test_book_add_review(dummy_book, dummy_review):
    dummy_book.add_review(dummy_review)
    assert dummy_book.rating == 4
    assert len(list(dummy_book.display_reviews())) == 1

def test_book_add_duplicate_review(dummy_book, dummy_review):
    dummy_book.add_review(dummy_review)
    with pytest.raises(Exception):
        dummy_book.add_review(dummy_review)

def test_book_delete_review(dummy_book, dummy_review):
    dummy_book.add_review(dummy_review)
    dummy_book.delete_review(dummy_review.user_id)
    assert len(list(dummy_book.display_reviews())) == 0
    assert dummy_book.rating is None


