import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def group_sentiment_by_newspaper(sentiment_file):
    """
    Aggregate the sentiment of articles by newspaper name.

    This function takes as input a CSV file that contains at least two columns: 
    "source_name" and "sentiment". Each row in the file represents the sentiment score 
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
        dataframe: A pandas dataframe where the newspaper names (from the "source_name" column) 
              and the aggregated sentiment scores (mean and median) for each newspaper. 
            The dataframe is sorted by the number of articles retrieved.

    Example:
        >>> sentiment_file = 'sentiment_data.csv'
        >>> group_sentiment_by_newspaper(sentiment_file)
                sentiment_mean  sentiment_contents_mean  sentiment_description_mean  sentiment_median  sentiment_contents_median  sentiment_description_median  article_count
        source_name
        Yahoo Entertainment       -0.450301                 0.304349                    0.347987         -0.698542                   0.395626                      0.395627             56
        Business Insider          -0.513429                -0.222577                   -0.425274         -0.756237                  -0.235422                     -0.740187             48
        ABC News                  -0.383447                -0.155162                   -0.344649         -0.632127                  -0.131075                     -0.433300             38

    Notes:
        - The CSV file is expected to have at least the columns "source_name" and "sentiment". If the 
          file format differs, an error may occur.
    """
    sentiment_file_fname = os.path.join(os.path.dirname('__file__'), sentiment_file)
    with open(sentiment_file_fname, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f)

    return df.groupby('source_name').agg(
        sentiment_mean=('sentiment', 'mean'),
        sentiment_contents_mean=('sentiment_contents', 'mean'),
        sentiment_description_mean=('sentiment_description', 'mean'),
        sentiment_median=('sentiment', 'median'),
        sentiment_contents_median=('sentiment_contents', 'median'),
        sentiment_description_median=('sentiment_description', 'median'),
        article_count=('title', 'count')
        ).sort_values(by='article_count', ascending=False).reset_index()

def plot_histogram(sentiment_file):
    sentiment_file_fname = os.path.join(os.path.dirname('__file__'), sentiment_file)
    with open(sentiment_file_fname, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f)
    
    print(f"Average Sentiment Score:\t{df['sentiment'].mean()}")
    print(f"Average Sentiment Contents Score:\t{df['sentiment_contents'].mean()}")
    print(f"Average Sentiment Description Score:\t{df['sentiment_description'].mean()}")
    print(f"Total Articles:\t{df.shape[0]}")

    plt.hist(df['sentiment'])
    plt.ylabel('Number of Articles')
    plt.xlabel('Sentiment Score')
    plt.show()

def plot_sentiment(sentiment_df):
    """
    Create png plots of the sentiment
    
    The plots generated were of the following (taking the top 5 sources with the most 
    articles retireved):
    - mean sentiment scores per newpaper source
    - median sentiment scores per newspaper source
    """
    # df = sentiment_df.head(5)

    x = np.arange(len(df['source_name']))
    bar_width = 0.25

    # plt.figure(figsize=(6,12))
    plt.barh(x - bar_width, df['sentiment_mean'], height=bar_width, label='Sentiment Mean')
    plt.barh(x, df['sentiment_contents_mean'], height=bar_width, label='Sentiment Contents Mean')
    plt.barh(x + bar_width, df['sentiment_description_mean'], height=bar_width, label='Sentiment Description Mean')

    # plt.title('Sentiment Metrics by Source Name')
    plt.xlabel('Sentiment Values')
    plt.yticks(x, df['source_name'])  # Set y-ticks as source names
    plt.ylabel('Source Name')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), prop={'size': 9})
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file', help='file path to processed and labelled dataset')
    args = parser.parse_args()

    plot_histogram(args.input_file)
    df = group_sentiment_by_newspaper(args.input_file)
    df = df[df['article_count'] >= 10]
    # print(dict['source_name'].to_numpy()[10:20])
    print(df)
    # print(list(dict.items())[:10])
    # plot_sentiment(df)