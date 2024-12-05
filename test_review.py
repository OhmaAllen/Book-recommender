import pytest
from Review import Review

@pytest.fixture
def dummy_review():
    return Review(user_rsp="Test User", isbn="1234567890", user_id=1, usr_rating=4, review="Great book!")

def test_review_initialization(dummy_review):
    assert dummy_review.user_rsp == "Test User"
    assert dummy_review.isbn == "1234567890"
    assert dummy_review.user_id == 1
    assert dummy_review.usr_rating == 4
    assert dummy_review.review == "Great book!"

def test_review_edit_review(dummy_review):
    dummy_review.review = "Updated review"
    assert dummy_review.review == "Updated review"
