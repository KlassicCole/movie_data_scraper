import os
import pandas as pd
from filter_datasets import filter_by_votes, filter_by_rating, filter_by_genre, exclude_watched_titles, exclude_vintage_films
from output_writer import save_to_excel

# Define Paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
datasets_dir = os.path.join(project_root, "datasets")

# Paths to the Merged Datasets
merged_movies_path = os.path.join(datasets_dir, 'restructured_datasets', 'combined', 'merged_us_english_movies.tsv')
merged_tvseries_path = os.path.join(datasets_dir, 'restructured_datasets', 'combined', 'merged_us_english_tvseries.tsv')

def load_merged_datasets():
    """Load the merged US and English datasets for movies and TV series."""
    print("Loading merged datasets...")
    movies_data = pd.read_csv(merged_movies_path, sep='\t', low_memory=False)
    tvseries_data = pd.read_csv(merged_tvseries_path, sep='\t', low_memory=False)
    return movies_data, tvseries_data

# Interactive filtering function
def interactive_filter(data, user_dir):
    """Interactively apply filters to the dataset."""
    print("Welcome to the Interactive Movie and TV Filter!")
    print("Choose filters to apply (e.g.,1,3):")
    print("1. Filter by Minimum Votes")
    print("2. Filter by Minimum Rating")
    print("3. Filter by Genre")
    print("4. No Filters (Proceed with all data)")

    # Get user selection
    selected_filters = input("Enter your choices (comma-separated): ").split(',')

    # Start with the original data
    filtered_data = data.copy()  # Work on a copy to avoid modifying the original dataset

    # Set default values to avoid 'referenced before assignment' error
    min_votes = 0  # Default: No minimum votes
    min_rating = 0  # Default: No minimum rating

    # HARD CODED Filters
    filtered_data = exclude_vintage_films(filtered_data, year_threshold=1960)
    print("Filtering for title newer than 1960...")

    # Apply selected filters
    for choice in selected_filters:
        choice = choice.strip()  # Clean up whitespace
        if choice == '1':
            # Filter by Minimum Votes
            min_votes = int(input("Enter the minimum number of votes required (e.g., 5000): "))
            filtered_data = filter_by_votes(filtered_data, min_votes)
        elif choice == '2':
            # Filter by Minimum Rating
            min_rating = float(input("Enter the minimum rating (e.g., 7.5): "))
            filtered_data = filter_by_rating(filtered_data, min_rating)
        elif choice == '3':
            # Filter by Genre
            genre = input("Enter the genre (e.g., Comedy): ")
            filtered_data = filter_by_genre(filtered_data, genre)
        elif choice == '4':
            # No filters
            print("Proceeding without additional filters.")
            break
        else:
            print(f"Invalid choice: {choice}. Skipping...")

    # Exclude watched titles for both movies and TV series
    watched_movies_file = os.path.join(user_dir, "cole_watched_movies.xlsx")
    filtered_data = exclude_watched_titles(filtered_data, watched_movies_file)

    watched_tvseries_file = os.path.join(user_dir, "cole_watched_tvseries.xlsx")
    filtered_data = exclude_watched_titles(filtered_data, watched_tvseries_file)

    return filtered_data, min_votes, min_rating

def main():
    # Paths and directories
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    datasets_dir = os.path.join(project_root, 'datasets', 'restructured_datasets', 'combined')
    outputs_dir = os.path.join(project_root, 'outputs')
    user_dir = os.path.join(project_root, 'usrdata', 'klassiccole')
    os.makedirs(outputs_dir, exist_ok=True)

    # Load merged datasets
    movies_data, tvseries_data = load_merged_datasets()

    # Apply filters once for movies and get filter values
    filtered_movies, min_votes, min_rating = interactive_filter(movies_data, user_dir)

    # Apply the same filters to TV series
    filtered_tvseries = tvseries_data.copy()
    filtered_tvseries = exclude_vintage_films(filtered_tvseries, year_threshold=1960)
    filtered_tvseries = filter_by_votes(filtered_tvseries, min_votes)
    filtered_tvseries = filter_by_rating(filtered_tvseries, min_rating)

    # Save outputs
    save_to_excel(filtered_movies, os.path.join(outputs_dir, "filtered_movies.xlsx"))
    save_to_excel(filtered_tvseries, os.path.join(outputs_dir, "filtered_tvseries.xlsx"))

    print("Process complete!")
    print("Filtered movies and TV series saved successfully.")

if __name__ == "__main__":
    main()
