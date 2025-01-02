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
combined_output_dir = os.path.join(output_dir, 'combined')
os.makedirs(combined_output_dir, exist_ok=True)


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

    return merged_data  # Return the merged dataset

def filter_by_region_and_save(merged_data):
    # Create subfolder for region-based files
    region_output_dir = os.path.join(output_dir, 'region')
    os.makedirs(region_output_dir, exist_ok=True)

    # Filter by Region (US)
    print("Filtering by region (US)...")
    filtered_data_us = merged_data[merged_data['region'] == 'US']
    print(f"Filtered to {len(filtered_data_us)} entries with region 'US'...")

    # Filter movies and TV series from the US dataset
    print("Filtering for movies and TV series in US dataset...")
    us_movies = filtered_data_us[filtered_data_us['titleType'] == 'movie']
    us_tvseries = filtered_data_us[filtered_data_us['titleType'] == 'tvSeries']

    # Save filtered data to new TSV files in the region folder
    print("Saving US filtered datasets...")
    us_movies.to_csv(os.path.join(region_output_dir, 'us_movies.tsv'), sep='\t', index=False)
    us_tvseries.to_csv(os.path.join(region_output_dir, 'us_tvseries.tsv'), sep='\t', index=False)

    print("Files saved in 'region' subfolder.")

def filter_by_language_and_save(merged_data):
    # Create subfolder for language-based files
    language_output_dir = os.path.join(output_dir, 'language')
    os.makedirs(language_output_dir, exist_ok=True)

    # Filter for English language titles
    print("Filtering for English language titles...")
    english_movies = merged_data[(merged_data['titleType'] == 'movie') & (merged_data['language'] == 'en')]
    english_tvseries = merged_data[(merged_data['titleType'] == 'tvSeries') & (merged_data['language'] == 'en')]

    # Save filtered data to new TSV files in the language folder
    print("Saving English filtered datasets...")
    english_movies.to_csv(os.path.join(language_output_dir, 'english_movies.tsv'), sep='\t', index=False)
    english_tvseries.to_csv(os.path.join(language_output_dir, 'english_tvseries.tsv'), sep='\t', index=False)

    print("Files saved in 'language' subfolder.")

def merge_us_and_english_movies():
    # Paths to the input files
    region_movies_path = os.path.join(output_dir, 'region', 'us_movies.tsv')
    language_movies_path = os.path.join(output_dir, 'language', 'english_movies.tsv')

    # Load datasets
    print("Loading US and English movies datasets for merging...")
    us_movies = pd.read_csv(region_movies_path, sep='\t', low_memory=False)
    english_movies = pd.read_csv(language_movies_path, sep='\t', low_memory=False)

    # Concatenate datasets (stacking rows)
    print("Concatenating datasets...")
    merged = pd.concat([us_movies, english_movies], ignore_index=True)

    # Remove duplicate 'tconst', keeping the first occurrence
    merged = merged.drop_duplicates(subset=['tconst'], keep='first')

    # Save the merged dataset
    output_file = os.path.join(combined_output_dir, 'merged_us_english_movies.tsv')
    merged.to_csv(output_file, sep='\t', index=False)

    print(f"Merged file saved as '{output_file}' in 'combined' folder.")

def merge_us_and_english_tvseries():
    # Paths to the input files
    region_tvseries_path = os.path.join(output_dir, 'region', 'us_tvseries.tsv')
    language_tvseries_path = os.path.join(output_dir, 'language', 'english_tvseries.tsv')

    # Load datasets
    print("Loading US and English TV series datasets for merging...")
    us_tvseries = pd.read_csv(region_tvseries_path, sep='\t', low_memory=False)
    english_tvseries = pd.read_csv(language_tvseries_path, sep='\t', low_memory=False)

    # Concatenate datasets (stacking rows)
    print("Concatenating TV series datasets...")
    merged = pd.concat([us_tvseries, english_tvseries], ignore_index=True)

    # Remove duplicate 'tconst', keeping the first occurrence
    merged = merged.drop_duplicates(subset=['tconst'], keep='first')

    # Save the merged dataset
    output_file = os.path.join(combined_output_dir, 'merged_us_english_tvseries.tsv')
    merged.to_csv(output_file, sep='\t', index=False)

    print(f"Merged file saved as '{output_file}' in 'combined' folder.")

if __name__ == "__main__":
    merged_data = load_and_merge_datasets()
    filter_by_region_and_save(merged_data)  # US filter
    filter_by_language_and_save(merged_data)  # English filter
    merge_us_and_english_movies() # Merge en and US filtered movies
    merge_us_and_english_tvseries() # Merge en and US filtered tvseries


