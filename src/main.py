import os
import pandas as pd
from filter_datasets import filter_by_votes, filter_by_rating, filter_by_genre, filter_by_language, exclude_watched_titles, exclude_vintage_films
from output_writer import save_to_excel

def load_dataset(file_path):
    """Loads a single dataset from a TSV file."""
    print(f"Loading datasets... {file_path}")
    return pd.read_csv(file_path, sep="\t", low_memory=False)

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

    # HARD CODED Filters
    # filtered_data = filter_by_language(filtered_data, 'en')
    # print("Filtering for English titles...")
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

    return filtered_data

def main():
    # Paths and directories
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    datasets_dir = os.path.join(project_root, "datasets", "restructured_datasets")
    outputs_dir = os.path.join(project_root, "outputs")
    user_dir = os.path.join(project_root, "usrdata", "klassiccole")
    os.makedirs(outputs_dir, exist_ok=True)

    # File paths
    movies_path = os.path.join(datasets_dir, "movies.tsv")
    tvseries_path = os.path.join(datasets_dir, "tvseries.tsv")

    # Load datasets
    movies_data = load_dataset(movies_path)
    tvseries_data = load_dataset(tvseries_path)

    # Prompt user for filters and apply the same logic to both datasets
    filtered_movies = interactive_filter(movies_data, user_dir)
    filtered_tvseries = tvseries_data.copy()

    # Apply the same filters to TV series without prompting again
    filtered_tvseries = filter_by_language(filtered_tvseries, 'en')
    filtered_tvseries = exclude_vintage_films(filtered_tvseries, year_threshold=1960)

    # Save outputs
    save_to_excel(filtered_movies, os.path.join(outputs_dir, "filtered_movies.xlsx"))
    save_to_excel(filtered_tvseries, os.path.join(outputs_dir, "filtered_tvseries.xlsx"))

    print("Process complete!")
    print("Filtered movies and TV series saved successfully.")

if __name__ == "__main__":
    main()
