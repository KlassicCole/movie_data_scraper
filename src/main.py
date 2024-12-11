from filter_datasets import filter_by_rating, filter_by_genre, filter_by_title_type, filter_by_votes, \
    exclude_watched_titles, exclude_vintage_films, filter_by_language
from output_writer import save_to_excel
import pandas as pd
import os

# Dynamically construct paths to datasets
base_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory of this script
project_dir = os.path.join(base_dir, '..')  # Move up to the project root
datasets_dir = os.path.join(project_dir, 'datasets')

# File paths
title_basics_path = os.path.join(datasets_dir, 'title.basics.tsv')
title_ratings_path = os.path.join(datasets_dir, 'title.ratings.tsv')
title_akas_path = os.path.join(datasets_dir, 'title.akas.tsv')

def load_datasets():
    """Loads and merges the datasets."""
    title_basics = pd.read_csv(title_basics_path, sep='\t', low_memory=False)
    title_ratings = pd.read_csv(title_ratings_path, sep='\t')
    title_akas = pd.read_csv(title_akas_path, sep='\t', low_memory=False)

    # Merge basics and ratings datasets
    merged_data = pd.merge(title_basics, title_ratings, on='tconst')

    return merged_data, title_akas

# Interactive filtering function
def interactive_filter(data, akas_data, user_dir):
    """Interactively apply filters to the dataset."""
    print("Welcome to the Interactive Movie and TV Filter!")
    print("1. Filter by Rating")
    print("2. Filter by Genre")
    print("3. Apply Both Filters")
    choice = input("Choose a filtering option (1/2/3): ")

    # Start with the original data
    filtered_data = data.copy()  # Ensure you're working on a copy, not modifying the original dataset

    # Hard filters
    filtered_data = filter_by_title_type(filtered_data, ['movie', 'tvSeries'])
    filtered_data = filter_by_votes(filtered_data, 50000)
    filtered_data = exclude_vintage_films(filtered_data, year_threshold=1960)

    # Prompt the user to filter by language
    language_choice = input("Enter the language code to filter by (e.g., 'en' for English, 'es' for Spanish). Leave blank to skip: ")
    if language_choice.strip():  # Only apply the filter if something is entered
        filtered_data = filter_by_language(filtered_data, akas_data, language_choice)
    else:
        print("Skipping language filter.")

    # Filter by rating
    if choice in ['1', '3']:
        min_rating = float(input("Enter the minimum rating (e.g., 7.5): "))
        filtered_data = filter_by_rating(filtered_data, min_rating)

    # Filter by genre
    if choice in ['2', '3']:
        genre = input("Enter the genre (e.g., Comedy): ")
        filtered_data = filter_by_genre(filtered_data, genre)

    # Exclude watched movies and TV series
    watched_movies_file = os.path.join(user_dir, 'cole_watched_movies.xlsx')
    filtered_movies = filtered_data[filtered_data['titleType'] == 'movie']
    filtered_movies = exclude_watched_titles(filtered_movies, watched_movies_file)

    watched_tvseries_file = os.path.join(user_dir, 'cole_watched_tvseries.xlsx')
    filtered_tvseries = filtered_data[filtered_data['titleType'] == 'tvSeries']
    filtered_tvseries = exclude_watched_titles(filtered_tvseries, watched_tvseries_file)

    return filtered_data, filtered_movies, filtered_tvseries

def main():
    # Define user-specific directory
    user_name = "klassiccole"  # Change this if you want to use a dynamic username
    user_dir = os.path.join(project_dir, 'usrdata', user_name)
    os.makedirs(user_dir, exist_ok=True)  # Create user-specific folder if it doesn't exist

    # Load the datasets
    full_data, akas_data = load_datasets()

    # Apply interactive filtering
    filter_data, filtered_movies, filtered_tvseries = interactive_filter(full_data, akas_data, user_dir)

    # Save the filtered datasets to separate Excel files
    outputs_dir = os.path.join(project_dir, 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)

    movies_file = os.path.join(outputs_dir, 'filtered_movies.xlsx')
    tvseries_file = os.path.join(outputs_dir, 'filtered_tvseries.xlsx')

    save_to_excel(filtered_movies, movies_file)
    save_to_excel(filtered_tvseries, tvseries_file)

    print(f"Filtered movies saved to {movies_file}")
    print(f"Filtered TV series saved to {tvseries_file}")
    print("Process complete!")

if __name__ == "__main__":
    main()
