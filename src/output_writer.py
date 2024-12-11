import pandas as pd

def save_to_excel(data, file_path):
    """
    Saves the DataFrame to an Excel file with a specified column order and removes unnecessary columns.

    Parameters:
        data (pd.DataFrame): The data to save.
        file_path (str): The path to save the Excel file.
    """
    # Columns to remove
    columns_to_remove = ['title', 'titleId', 'ordering', 'types', 'attributes', 'isOriginalTitle', 'isAdult']

    # Remove unwanted columns
    data = data.drop(columns=columns_to_remove, errors='ignore')

    # Define the desired column order (with startYear, endYear, titleType, and tconst at the end)
    columns = list(data.columns)  # Get current column order
    for col in ['tconst', 'titleType', 'startYear', 'endYear']:
        if col in columns:
            columns.remove(col)  # Temporarily remove these columns if they exist

    # Append the desired columns at the end
    desired_order = columns + ['startYear', 'endYear', 'titleType', 'tconst']

    # Reorder columns
    data = data.reindex(columns=desired_order)

    # Save to Excel
    data.to_excel(file_path, index=False, engine='openpyxl')
    print(f"Data saved to {file_path}")


def save_to_csv(data: pd.DataFrame, file_path: str) -> None:
    """
    Saves the given DataFrame to a CSV file.
    Parameters:
        data (pd.DataFrame): The dataset to save.
        file_path (str): The full path to save the CSV file.
    Returns:
        None
    """
    try:
        data.to_csv(file_path, index=False)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")
