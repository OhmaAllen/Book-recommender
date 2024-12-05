import pytest
from User import User
from Review import Review

@pytest.fixture
def dummy_user():
    return User(user_id=1, name="Test User", email="test@example.com")

@pytest.fixture
def dummy_review():
    return Review(user_rsp="Test User", isbn="1234567890", user_id=1, usr_rating=4, review="Great book!")

def test_user_initialization(dummy_user):
    assert dummy_user.user_id == 1
    assert dummy_user.name == "Test User"
    assert dummy_user.info == {"email": "test@example.com"}
    assert dummy_user.reviews == {}

def test_user_add_review(dummy_user, dummy_review):
    dummy_user.add_review(dummy_review)
    assert dummy_review.isbn in dummy_user.reviews

def test_user_add_duplicate_review(dummy_user, dummy_review):
    dummy_user.add_review(dummy_review)
    with pytest.raises(Exception):
        dummy_user.add_review(dummy_review)

def test_user_delete_review(dummy_user, dummy_review):
    dummy_user.add_review(dummy_review)
    dummy_user.delete_review(dummy_review.isbn)
    assert dummy_review.isbn not in dummy_user.reviews
