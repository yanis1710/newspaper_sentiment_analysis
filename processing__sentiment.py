
from models import *
import requests
from bs4 import BeautifulSoup

def fetch_article_content(url):
    """
    Fetches the main content of a web page by extracting all text within the <article> tag.

    Parameters:
    url (str): The URL of the web page from which the article content is to be fetched.

    Returns:
    str or None: Returns the text content of the <article> tag if found, or None if:
        - The request to the URL fails (non-200 status code).
        - No <article> tag is found in the page.

    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # First, try to find the <article> tag
        article = soup.find('article')

        # If <article> tag is not found, search for <main>
        if not article:
            article = soup.find('main')

        # Check if the article tag exists
        if article:
            # Extract the content within the article tag
            article_text = article.get_text()
            return article_text.strip()
        else:
            return None
    else:
        return None
    
def clean_text(text):
    pass


#TODO
def assign_sentiment(raw_file):
    """
    Assign sentiment scores to articles based on their content.

    This function takes a raw CSV file that contains a column "content", where each row 
    represents an article. It reads the content of each article and assigns a sentiment score 
    using a sentiment analysis model (imported from `models.py`). The sentiment score is 
    then added as a new column, "sentiment", to the CSV file.

    The function processes each article individually, computes its sentiment, and stores the 
    result in the "sentiment" column. It then returns the updated dataframe with the 
    sentiment scores.

    Args:
        raw_file (str): The path to the raw CSV file containing the "content" column, where 
                         each row corresponds to an article's text.

    Returns:
        pd.DataFrame: A pandas DataFrame with an additional "sentiment" column, where each 
                      value represents the sentiment of the corresponding article.

    Example:
        >>> raw_file = 'articles.csv'
        >>> df = assign_sentiment(raw_file)
        >>> df.head()
        title        content                           sentiment
        Article 1    This is great news!               0.9
        Article 2    I'm upset about this development.  -0.6
        Article 3    Neutral perspective here.          0.0

    Notes:
        - The sentiment analysis model used to compute the sentiment score must be 
          imported from `models.py`.
        - The function assumes the CSV file has at least the "content" column, and 
          may not work correctly if this column is missing.
    """
    pass


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

if __name__ == "__main__":
    url = 'https://www.bbc.com/sport/snooker/articles/c7042p2k1q5o'
    url = 'https://www.theverge.com/2024/12/13/24320515/trump-tesla-crash-reporting-adas-nhtsa-sgo'
    #url = 'https://gizmodo.com/trump-reportedly-set-to-attend-sixth-spacex-starship-launch-today-2000526481'
    #url = 'https://www.npr.org/2024/11/17/1213718584/from-trump-opponent-to-trump-loyalist-the-evolution-of-marco-rubio'

    content = fetch_article_content(url)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(content)

