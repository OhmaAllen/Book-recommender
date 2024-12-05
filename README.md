# Book Recommendation System

## Project Overview

This is a sophisticated Book Recommendation System that leverages vector-based recommendation techniques to help users discover new books based on their reading preferences and review patterns.

## Project Structure

```
project/
│
├── main.py                     # Application entry point
├── ApplicationInterface.py     # Core application logic
│
├── Core Classes:
│   ├── Author.py               # Author class implementation
│   ├── Book.py                 # Book class definition
│   ├── User.py                 # User management and interactions
│   └── Review.py               # Review class implementation
│
├── Recommendation Engine:
│   ├── RecommendationEngine.py # Abstract base class for recommendations
│   └── VectorRecommendationEngine.py # Vector-based recommendation logic
│
├── User Interface:
│   ├── UserInterface.py        # Command-line interaction module
│
├── Utilities:
│   └── tools.py                # Data handling and utility functions
│
├── Dataset:
│   ├── books_data.csv          # Books information dataset
│   └── Books_rating.csv        # User reviews and ratings dataset
│
└── tests/                      # Unit testing directory
```

## Features

- Vector-based book recommendation algorithm
- User profile and review management
- Comprehensive book and author tracking
- Command-line interface for easy interaction

