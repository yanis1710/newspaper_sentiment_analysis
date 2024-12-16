
from models import *
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd

# Download required NLTK resources (only once)
def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt_tab')

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
            return ""
    else:
        return ""
    
def clean_article_content(raw_text):
    """
    Cleans and preprocesses the raw text extracted from a webpage with NLP preprocessing steps.
    
    Args:
        raw_text (str): The raw text extracted from the webpage.
        
    Returns:
        str: The cleaned and preprocessed text.
    """
    # Remove unwanted special characters (extra spaces, newlines, etc.)
    cleaned_text = re.sub(r'\s+', ' ', raw_text)  # Replace multiple spaces or newlines with a single space
    cleaned_text = cleaned_text.strip()  # Remove leading and trailing spaces

    # Remove any non-ASCII characters (optional, depending on your use case)
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)

    # Remove URLs and email addresses
    cleaned_text = re.sub(r'http[s]?://\S+', '', cleaned_text)  # Remove URLs
    cleaned_text = re.sub(r'\S+@\S+', '', cleaned_text)  # Remove email addresses

    # Remove unnecessary punctuation or symbols
    cleaned_text = re.sub(r'[^\w\s,.!?-]', '', cleaned_text)  # Keep only alphanumeric and basic punctuation

    # Convert to lowercase
    cleaned_text = cleaned_text.lower()

    # Tokenize the text into words
    words = word_tokenize(cleaned_text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Lemmatize words (convert them to their root form)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

    # Rejoin words back into a single string
    final_text = ' '.join(lemmatized_words)

    return final_text

def raw_to_clean_dataset_with_sentiment(raw_file):
    """
    Read a CSV file containing URLs, fetch the article content, and clean the text.

    Args:
        raw_file (str): The path to the raw CSV file containing URLs.

    Returns:
        pd.DataFrame: A DataFrame with the original URLs and their cleaned content.
    """
    # Read the CSV file
    df = pd.read_csv(raw_file)
    download_nltk_resources()


    # Fetch article content for each URL and clean the text
    # Create a new file or overwrite existing one to store raw content
    df['content'] = df['URL'].apply(lambda url: clean_article_content(fetch_article_content(url)))
    clean_file = raw_file.replace("Raw_Datasets", "Clean_Datasets")
    df.to_csv(clean_file, index=False)
    
    # df['sentiment'] = df['content'].apply(lambda content: sentiment_analyzer(content))
    df['sentiment'] = sentiment_analyzer(df['title'])
    df['sentiment_contents'] = sentiment_analyzer(df['content'])
    df['sentiment_description'] = sentiment_analyzer(df['description'])

    return df    

if __name__ == "__main__":
    #url = 'https://www.bbc.com/sport/snooker/articles/c7042p2k1q5o'
    #url = 'https://www.theverge.com/2024/12/13/24320515/trump-tesla-crash-reporting-adas-nhtsa-sgo'
    #url = 'https://gizmodo.com/trump-reportedly-set-to-attend-sixth-spacex-starship-launch-today-2000526481'
    #url = 'https://www.npr.org/2024/11/17/1213718584/from-trump-opponent-to-trump-loyalist-the-evolution-of-marco-rubio'

    #content = fetch_article_content(url)
    #with open("output.txt", "w", encoding="utf-8") as f:
        #f.write(content)
        
    df = raw_to_clean_dataset_with_sentiment("Raw_Datasets/news_articles_Trump.csv")
    df.to_csv("Clean_Datasets/Clean_news_articles_Trump.csv")
    print(df)

