import pandas as pd

def filter_by_title_type(data, allowed_types):
    """
    Filters the dataset to include only the specified title types.
    Parameters:
        data (pd.DataFrame): The dataset to filter.
        allowed_types (list): A list of allowed title types (e.g., ['movie', 'tvSeries']).
    Returns:
        pd.DataFrame: Filtered DataFrame with only the allowed title types.
    """
    return data[data['titleType'].isin(allowed_types)]

def exclude_vintage_films(data, year_threshold=1960):
    """
    Excludes films released before a specified year.

    Parameters:
        data (pd.DataFrame): The dataset to filter.
        year_threshold (int): The earliest allowed year (default is 1960).

    Returns:
        pd.DataFrame: Filtered DataFrame excluding vintage films.
    """
    # Ensure 'startYear' is numeric, as it might contain invalid values
    data['startYear'] = pd.to_numeric(data['startYear'], errors='coerce')

    # Filter out rows with startYear less than the threshold
    return data[data['startYear'] >= year_threshold]

def filter_by_language(data, akas_data, language):
    """
    Filters the dataset to include titles available in a specific language.

    Parameters:
        data (pd.DataFrame): The main dataset.
        akas_data (pd.DataFrame): The title.akas dataset.
        language (str): The language to filter by (e.g., "en" for English).

    Returns:
        pd.DataFrame: Filtered DataFrame with titles matching the specified language.
    """
    # Filter akas_data by the specified language
    akas_filtered = akas_data[akas_data['language'] == language]

    # Merge the main dataset with the filtered akas data
    merged_data = pd.merge(data, akas_filtered, left_on='tconst', right_on='titleId')

    # Drop duplicates based on the original tconst from the main dataset
    deduplicated_data = merged_data.drop_duplicates(subset='tconst')

    return deduplicated_data

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


