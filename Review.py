class Review:
    def __init__(self, user_rsp, isbn, user_id, usr_rating, review):
        self.__user_rsp = user_rsp
        self.__isbn = isbn
        self.__user_id = user_id
        self.__usr_rating = usr_rating
        self.__review = review

    @property
    def user_rsp(self):
        return self.__user_rsp

    @property
    def isbn(self):
        return self.__isbn

    @property
    def user_id(self):
        return self.__user_id

    @property
    def usr_rating(self):
        return self.__usr_rating
    
    @property
    def review(self):
        return self.__review
    
    # setter for review
    @review.setter
    def review(self, review):
        self.__review = review

    def __hash__(self) -> int:
        # return hash(self.__user_rsp)
        return hash((self.__user_id, self.__isbn))

    def __repr__(self):
        return (
            f"Review(user_rsp={self.__user_rsp}, isbn={self.__isbn}, "
            f"user_id={self.__user_id}, usr_rating={self.__usr_rating}, text={self.__review})"
        )
