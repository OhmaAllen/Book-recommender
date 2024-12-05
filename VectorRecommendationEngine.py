from RecommendationEngine import RecommendationEngine
from sklearn.neighbors import NearestNeighbors

from transformers import AutoModel, AutoTokenizer
from Book import Book
from User import User
from tools import Vectorizer
from tqdm import tqdm
import torch
import os 
import numpy as np
from gensim.models import KeyedVectors


class VectorRecommendationEngine(RecommendationEngine):
    def __init__(self, device='cuda'):
        super().__init__()
        self.__vectorizer = Vectorizer()
        try:
            self.__vectorizer.to(device)
        except:
            self.__vectorizer.cpu()

        try:
            self.__space = KeyedVectors(vector_size=self.dim)
        except:
            self.__space = KeyedVectors(dim=self.dim)

        print(f'{self.__vectorizer.device}')
        

    def recommend_for_user(self, user: User, top_k=10) -> list[str, float]:
        user_interest_vector = np.zeros(self.__vectorizer.dim)
        for review in user.reviews.values():
            
            user_interest_vector += self.__space[review.isbn] * (review.usr_rating - 3)
        reviewed_books = [review for review in user.reviews] # we would like to exclude the reviewed books from the results
        print(type(user_interest_vector))
        # get top_k+1 nearest neighbors because the user itself might be included
        candidates = self.__space.similar_by_vector(user_interest_vector, topn=top_k+len(reviewed_books))
        
        filtered_candidates = [
            (isbn, score) for isbn, score in candidates if isbn not in reviewed_books
        ]
        return filtered_candidates[:top_k]
        

    def recommend_for_book(self, book: Book, top_k=10) -> list[(str, float)]:
        # get top_k+1 nearest neighbors because the book itself might be included
        candidates: list[(str, float)] = self.__space.most_similar(book.isbn, topn=top_k+1)
        # remove book from the list
        filtered_candidates = [
            (isbn, score) for isbn, score in candidates if isbn != book.isbn
        ]
        return filtered_candidates[:top_k]
        
    @property
    def vectorizer(self):
        return self.__vectorizer
        

    # batch update
    def fit(self, data, batch_size=256):
        if not isinstance(data, list):
            data = list(data)
        vectors = torch.empty((len(data), self.__vectorizer.dim), device=self.__vectorizer.device)

        keys = [book.isbn for book in data]
        if os.path.exists('space.pkl'):
            self.__space = KeyedVectors.load('space.pkl')
            return
        with torch.no_grad():
            for i in tqdm(range(0, len(data), batch_size)):
                batch = data[i:min(i+batch_size, len(data))]
                book_list = [book.representation() for book in batch]
                vectors[i:min(i+batch_size, len(data))] = self.__vectorizer(book_list)
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
            self.__space.add_vectors(keys, vectors.cpu().numpy())
        
    

    def update(self, data):
        # book
        if isinstance(data, Book):
            key = data.isbn
            vector = self.__vectorizer(data.representation)
            # check if book already in the vector space

            if key in self.__space:
                self.__space[key] = vector
            else:
                self.__space.add_vector(key, vector)
            
        if isinstance(data, list):
            pass
        
        
    @property
    def dim(self):
        return self.__vectorizer.dim

    @property
    def device(self):
        return self.__vectorizer.device
    
    def to(self, device):
        self.__vectorizer.to(device)

        return self
    
    
    
    
        

