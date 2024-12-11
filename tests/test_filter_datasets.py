import os
import pandas as pd
from src.filter_datasets import filter_by_rating, filter_by_genre

# Dynamically construct paths to datasets
base_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory of this script
datasets_dir = os.path.join(base_dir, '..', 'datasets')  # Move up to project root and into 'datasets'

# Load a sample dataset
data = pd.read_csv('datasets/title.basics.tsv', sep='\t', low_memory=False)
ratings = pd.read_csv('datasets/title.ratings.tsv', sep='\t')
full_data = pd.merge(data, ratings, on='tconst')

# Test filtering by rating
high_rated = filter_by_rating(full_data, 8.0)
print("High-rated movies:")
print(high_rated.head())

# Test filtering by genre
comedy_movies = filter_by_genre(full_data, "Comedy")
print("\nComedy movies:")
print(comedy_movies.head())