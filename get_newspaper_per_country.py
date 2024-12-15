from newsapi import NewsApiClient

def get_sources_for_country(country, api_key_file):
    """
    Fetches the names of news sources available in the specified country.

    Args:
        country (str): The country code (e.g., 'us' for the United States) for which to fetch news sources.
        api_key_file (str): The path to the file containing the NewsAPI key.

    Returns:
        list: A list of names of news sources available in the specified country.
        If the request fails, returns an empty list.
    """
    # Read the API key from the file
    with open(api_key_file, 'r') as file:
        api_key = file.read().strip()

    # Initialize the NewsApiClient
    newsapi = NewsApiClient(api_key=api_key)

    # Get sources from the specified country
    response = newsapi.get_sources(country=country)

    # Check if the request was successful
    if response['status'] == 'ok':
        # Extract the source names
        sources = response.get('sources', [])
        
        # Extract and print the names of the sources
        source_names = [source['id'] for source in sources]
        
        return source_names
    else:
        print("Failed to fetch sources")
        return []

if __name__ == "__main__":
    # Example usage
    api_key_file = 'api_key.txt'
    us_sources = get_sources_for_country('us', api_key_file)
    print("Sources from the US:")
    print(us_sources)
