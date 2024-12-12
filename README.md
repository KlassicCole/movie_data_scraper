```
  __  __            _        _____        _           _____
 |  \/  |          (_)      |  __ \      | |         / ____|
 | \  / | _____   ___  ___  | |  | | __ _| |_ __ _  | (___   ___ _ __ __ _ _ __   ___ _ __
 | |\/| |/ _ \ \ / / |/ _ \ | |  | |/ _` | __/ _` |  \___ \ / __| '__/ _` | '_ \ / _ \ '__|
 | |  | | (_) \ V /| |  __/ | |__| | (_| | || (_| |  ____) | (__| | | (_| | |_) |  __/ |
 |_|  |_|\___/ \_/ |_|\___| |_____/ \__,_|\__\__,_| |_____/ \___|_|  \__,_| .__/ \___|_|
                                                                          |_|
```
------------
**Overview**
------------
-The Movie Data Scraper is a Python-based program designed to process large IMDb datasets and generate customized Excel reports.
-filters movies and TV series based on various criteria, such as ratings, genres, languages, and more.
```
  ______         _                       
 |  ____|       | |                      
 | |__ ___  __ _| |_ _   _ _ __ ___  ___ 
 |  __/ _ \/ _` | __| | | | '__/ _ \/ __|
 | | |  __/ (_| | |_| |_| | | |  __/\__ \
 |_|  \___|\__,_|\__|\__,_|_|  \___||___/     
```                            
----------------------------------------------------------------
**Dataset Processing - Handles large IMDb datasets, including:**
----------------------------------------------------------------
    title.basics.tsv for general title information.
    title.ratings.tsv for ratings and votes.
    title.akas.tsv for alternate titles and languages.

-------------------------
**Interactive Filtering**
-------------------------
    Filter by rating (e.g., movies with a minimum rating of 8.0).
    Filter by genre (e.g., Comedy, Action).
    Filter by language (e.g., English, Spanish).

#These variables must be modified in the code.

    Exclude "vintage" films older than a specified year. The default is 1960.
    Exclude movies or TV series with fewer than a specified number of votes.

----------------------------
**User-Specific Exclusions**
----------------------------
-Excludes titles that the user has already watched based on user-defined Excel files.
-Outputs two separate Excel files:

    filtered_movies.xlsx: Contains filtered movies.
    filtered_tvseries.xlsx: Contains filtered TV series.

---------------------------------
**Optimized Column Presentation**
---------------------------------
-Removes unnecessary columns and reorders key columns, placing tconst, titleType, startYear, and endYear at the end.
```
 _____                               _     _ _            
|  __ \                             (_)   (_) |           
| |__) | __ ___ _ __ ___  __ _ _   _ _ ___ _| |_ ___  ___
|  ___/ '__/ _ \ '__/ _ \/ _` | | | | / __| | __/ _ \/ __|
| |   | | |  __/ | |  __/ (_| | |_| | \__ \ | ||  __/\__ \
|_|   |_|  \___|_|  \___|\__, |\__,_|_|___/_|\__\___||___/
                            | |                           
                            |_|
```
-Python 3.8 or higher.
-Virtual environment recommended for dependency management.
-Required Python packages
    pandas
    openpyxl

---------
**Usage**
---------
1. Prepare the Datasets
2. Place the IMDb datasets (.tsv files) in the datasets/ folder. Ensure the required datasets are available:

    **title.basics.tsv**
    **title.ratings.tsv**
    **title.akas.tsv**

- These datasets are distributed for non-Commercial use on the IMDB website.

3. Set Up Watched Lists
-Add user-specific watched lists (Excel files) to the usrdata/<username>/ folder.
-Example:

   **cole_watched_movies.xlsx for movies.**
   **cole_watched_tvseries.xlsx for TV series.**

4. Run the Program
-Execute the program from the command line:

    **python src/main.py**

5. Follow Interactive Prompts
The program will guide you through various filtering options, such as:

   **Minimum rating (e.g., 8.0)**
   **Genre (e.g., Comedy, Action)**
   **Language (e.g., English, Spanish)**

6. Output
The program generates two Excel files in the outputs/ folder:

