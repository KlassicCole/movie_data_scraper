import pandas as pd
import os

# Paths to original datasets
base_dir = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(base_dir, '../datasets')
output_dir = os.path.join(datasets_dir, 'restructured_datasets')

title_basics_path = os.path.join(datasets_dir, 'title.basics.tsv')
title_ratings_path = os.path.join(datasets_dir, 'title.ratings.tsv')
title_akas_path = os.path.join(datasets_dir, 'title.akas.tsv')

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def load_and_merge_datasets():
    # Load datasets
    print("Loading datasets...")
    basics = pd.read_csv(title_basics_path, sep='\t', low_memory=False)
    ratings = pd.read_csv(title_ratings_path, sep='\t')
    akas = pd.read_csv(title_akas_path, sep='\t', low_memory=False)

    # Rename 'titleId' to 'tconst' in akas to match other datasets
    print("Renaming 'titleId' to 'tconst' in akas dataset...")
    akas.rename(columns={'titleId': 'tconst'}, inplace=True)

    # Merge basics, ratings, and akas datasets
    print("Merging datasets...")
    merged_data = pd.merge(basics, ratings, on='tconst', how='inner')
    merged_data = pd.merge(merged_data, akas, on='tconst', how='left')

    # Deduplicate

    # Sort so English ('en') titles appear first, ensuring they're retained in case of duplicates
    merged_data = merged_data.sort_values(by=['language'], ascending=False)

    # Drop duplicates, keeping the first occurrence (which will now prioritize 'en' due to sorting)
    merged_data = merged_data.drop_duplicates(subset=['tconst'], keep='first')

    # Left join to keep all titles
    print("Deduplication complete...")

    return merged_data

def filter_and_save(merged_data):
    # Filter movies and TV series
    print("Filtering for movies and TV series...")
    movies = merged_data[merged_data['titleType'] == 'movie']
    tvseries = merged_data[merged_data['titleType'] == 'tvSeries']

    # Save filtered data to new TSV files
    print("Saving filtered datasets...")
    movies.to_csv(os.path.join(output_dir, 'movies.tsv'), sep='\t', index=False)
    tvseries.to_csv(os.path.join(output_dir, 'tvseries.tsv'), sep='\t', index=False)

    print("Files saved successfully as 'movies.tsv' and 'tvseries.tsv' in 'restructured_databases' folder.")

if __name__ == "__main__":
    merged_data = load_and_merge_datasets()
    filter_and_save(merged_data)

