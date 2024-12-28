import pandas as pd
    # Filter out rows with startYear less than the threshold
def exclude_vintage_films(data, year_threshold=1960):
    """Excludes films released before a specified year."""
    # Ensure 'startYear' is numeric, as it might contain invalid values
    data['startYear'] = pd.to_numeric(data['startYear'], errors='coerce')
    return data[data['startYear'] >= year_threshold]

def filter_by_language(data, language='en'):
    """Filters the dataset to only include titles in the specified language."""
    return data[data['language'] == language]

def filter_by_votes(data, min_votes):
    """
    Filters the dataset to include only titles with at least a specified number of votes.
    Parameters:
        data (pd.DataFrame): The dataset to filter.
        min_votes (int): The minimum number of votes required.
    Returns:
        pd.DataFrame: Filtered DataFrame with titles meeting the vote threshold.
    """
    return data[data['numVotes'] >= min_votes]

def filter_by_rating(data: pd.DataFrame, min_rating: float) -> pd.DataFrame:
    """
    Filters the movies in the dataset by a minimum rating.
    Parameters:
        data (pd.DataFrame): The movie dataset.
        min_rating (float): The minimum average rating.
    Returns:
        pd.DataFrame: Filtered DataFrame with movies above the given rating.
    """
    return data[data['averageRating'] >= min_rating]

def filter_by_genre(data: pd.DataFrame, genre: str) -> pd.DataFrame:
    """
    Filters the movies in the dataset by genre.
    Parameters:
        data (pd.DataFrame): The movie dataset.
        genre (str): The genre to filter by (e.g., "Comedy", "Drama").
    Returns:
        pd.DataFrame: Filtered DataFrame with movies matching the genre.
    """
    return data[data['genres'].str.contains(genre, na=False)]

def exclude_watched_titles(data, watched_file_path):
    """
    Excludes titles (movies or TV series) listed in a watched Excel file.
    Parameters:
        data (pd.DataFrame): The dataset to filter.
        watched_file_path (str): The path to the Excel file containing watched titles.
    Returns:
        pd.DataFrame: Filtered DataFrame excluding watched titles.
    """
    try:
        # Read watched titles from the Excel file
        watched_data = pd.read_excel(watched_file_path)

        # Assume the column with titles is named 'primaryTitle'
        watched_titles = set(watched_data['primaryTitle'])

        # Exclude titles whose names match the watched list
        return data[~data['primaryTitle'].isin(watched_titles)]
    except FileNotFoundError:
        print(f"Watched file not found: {watched_file_path}. Proceeding without exclusions.")
        return data
    except KeyError:
        print(f"'primaryTitle' column not found in {watched_file_path}. Proceeding without exclusions.")
        return data


