import os
import pandas as pd
from newsapi import NewsApiClient
from datetime import datetime, timedelta

def fetch_news_articles(search_term, api_key_file, page_size=100):
    # Read the News API key from the file
    with open(api_key_file, 'r') as file:
        api_key = file.read().strip()

    # Initialize the NewsApiClient
    newsapi = NewsApiClient(api_key=api_key)

    # Prepare a list to hold the data
    all_articles = []

    # Determine the CSV file path
    search_term_filename = search_term.replace(" ", "_")
    csv_filename = os.path.join('Raw_Datasets', f'news_articles_{search_term_filename}.csv')

    # Read existing articles from the CSV file if it exists
    if os.path.exists(csv_filename):
        existing_df = pd.read_csv(csv_filename)
        existing_titles = set(existing_df['title']) # Set of articles already read
    else:
        existing_titles = set()

    # Read all articles from last 30 days (Interval allowed by the NewsAPI)
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()

    # Iterate day by day to bypass the 100 request limit
    while True:
        print("NEW REQUEST")
        # Fetch articles from specific country sources only
        response = newsapi.get_everything(
            qintitle=search_term,
            from_param=start_date.strftime('%Y-%m-%d'),
            to=end_date.strftime('%Y-%m-%d'),
            language='en',
            sort_by='relevancy',
            page_size=page_size,
            page=1
        )

        # Check if the request was successful
        if response['status'] == 'ok':
            articles = response.get('articles', [])

            # If no articles are found, break the loop
            if not articles:
                break

            # Extract and append the data, avoiding duplicates
            for article in articles:
                title = article['title']
                if title not in existing_titles:
                    source_name = article['source']['name']
                    published_at = article['publishedAt']
                    url = article['url']
                    description = article['description']

                    all_articles.append({
                        'title': title,
                        'source_name': source_name,
                        'published_at': published_at,
                        'URL': url,
                        'description': description
                    })
                    existing_titles.add(title)  # Add the new title to the set of existing titles

            # Move the start date up by 1 days and adjust the start_date
            start_date =  min(start_date + timedelta(days=1), end_date)
            if start_date == end_date:
                break
        else:
            print(f"Failed to fetch articles: {response}")
            break

    # Create a DataFrame to display the results
    df = pd.DataFrame(all_articles)

    # Ensure the Raw_Datasets folder exists
    os.makedirs('Raw_Datasets', exist_ok=True)

    # Check if the CSV file exists
    if os.path.exists(csv_filename):
        # If it exists, append to the existing file without writing the header
        df.to_csv(csv_filename, mode='a', header=False, index=False)
    else:
        # If it does not exist, write the DataFrame to a new file with the header
        df.to_csv(csv_filename, index=False)

    return df

if __name__ == "__main__":
    api_key_file = 'api_key.txt'
    search_term = 'Trump'
    df = fetch_news_articles(search_term, api_key_file)
    print(df)
