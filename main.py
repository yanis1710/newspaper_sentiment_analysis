# TODO
def group_sentiment_by_newspaper(sentiment_file):
    """
    Aggregate the sentiment of articles by newspaper name.

    This function takes as input a CSV file that contains at least two columns: 
    "name" and "sentiment". Each row in the file represents the sentiment score 
    given to a specific article from a particular newspaper. The function groups 
    the data by the "name" (which represents the newspaper or source) and aggregates 
    the sentiment scores, either by calculating the mean or median of the sentiments 
    for each newspaper. It then returns a dictionary where the key is the newspaper 
    name ("name"), and the value is the aggregated sentiment score.

    Args:
        sentiment_file (str): The path to the CSV file containing the "name" and 
                               "sentiment" columns, among others. Each row represents 
                               an article's sentiment from a specific newspaper.

    Returns:
        dict: A dictionary where the keys are newspaper names (from the "name" column) 
              and the values are the aggregated sentiment scores (mean or median) for each newspaper.

    Example:
        >>> sentiment_file = 'sentiment_data.csv'
        >>> group_sentiment_by_newspaper(sentiment_file)
        {
            'New York Times': 0.32,
            'Washington Post': -0.15,
            'BBC News': 0.50
        }

    Notes:
        - The CSV file is expected to have at least the columns "name" and "sentiment". If the 
          file format differs, an error may occur.
    """
    pass

# TODO 
def plot_sentiment():
    pass
