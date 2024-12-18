import os
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# TODO which journals are most positive vs negative
# TODO time to sentiment mapping
# TODO mapping the journal articles to the timeframe

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
                source_name  sentiment_mean  sentiment_contents_mean  sentiment_description_mean  article_count  average_sentiment
        0  Yahoo Entertainment       -0.450301                 0.304349                    0.347987             56           0.067345
        1     Business Insider       -0.513429                -0.222577                   -0.425274             48          -0.387093
        2             ABC News       -0.383447                -0.155162                   -0.344649             38          -0.294419

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
            article_count=('title', 'count')
        ).assign(
            average_sentiment=lambda x: x[['sentiment_mean', 'sentiment_contents_mean', 'sentiment_description_mean']].mean(axis=1)
        ).sort_values(by='article_count', ascending=False).reset_index()

def plot_histogram(sentiment_file):
    sentiment_file_fname = os.path.join(os.path.dirname('__file__'), sentiment_file)
    with open(sentiment_file_fname, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f)

    df['average_sentiment'] = df[['sentiment', 'sentiment_contents', 'sentiment_description']].mean(axis=1)
    
    print(f"Average Sentiment Title Score:\t{df['sentiment'].mean()}")
    print(f"Average Sentiment Contents Score:\t{df['sentiment_contents'].mean()}")
    print(f"Average Sentiment Description Score:\t{df['sentiment_description'].mean()}")
    print(f"All Average Sentiment:\t{df['average_sentiment'].mean()}")
    print(f"Total Articles:\t{df.shape[0]}")

    # plt.figure(figsize=(4,6))
    # plt.subplot(411).hist(df['sentiment'])
    # plt.title('A'), plt.ylabel('Number of Articles'), plt.xlabel('Sentiment Score'), plt.xlim([-1.0, 1.0])
    # plt.subplot(412).hist(df['sentiment_contents'])
    # plt.title('B'), plt.ylabel('Number of Articles'), plt.xlabel('Sentiment Score'), plt.xlim([-1.0, 1.0])
    # plt.subplot(413).hist(df['sentiment_description'])
    # plt.title('C'), plt.ylabel('Number of Articles'), plt.xlabel('Sentiment Score'), plt.xlim([-1.0, 1.0])
    # plt.subplot(414).hist(df['average_sentiment'])
    # plt.title('D'), plt.ylabel('Number of Articles'), plt.xlabel('Sentiment Score'), plt.xlim([-1.0, 1.0])
    plt.hist(df['average_sentiment'])
    plt.ylabel('Number of Articles'), plt.xlabel('Sentiment Score'), plt.xlim([-1.0, 1.0])
    plt.tight_layout()
    plt.show()

def top_sentiment_articles(sentiment_file, output_fname):
    """
    Retrieve the articles with the most negative and positive sentiments
    """
    sentiment_file_fname = os.path.join(os.path.dirname('__file__'), sentiment_file)
    with open(sentiment_file_fname, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f)
    
    df['average_sentiment'] = df[['sentiment', 'sentiment_contents', 'sentiment_description']].mean(axis=1)
    sorted_df = df.sort_values('average_sentiment')

    data = [
        sorted_df.head(5)[['source_name', 'sentiment', 'sentiment_contents', 'sentiment_description', 'average_sentiment']].to_dict(),
        sorted_df.tail(5)[['source_name', 'sentiment', 'sentiment_contents', 'sentiment_description', 'average_sentiment']].to_dict()
    ]
    output_fname = os.path.join(os.path.dirname('__file__'), output_fname)
    with open(output_fname, 'w') as f:
        json.dump(data, f, indent=4)

    # return df.head(5), df.tail(5)

def plot_sentiment_all(sentiment_df):
    plt.barh(df['source_name'], df['average_sentiment'])

    plt.xlabel('Sentiment Values'), plt.xlim([-1.0, 1.0])
    plt.yticks(df['source_name'])
    plt.ylabel('Source Name')

    plt.tight_layout()
    plt.show()

def plot_sentiment(sentiment_df):
    """
    Create png plots of the sentiment
    
    The plots generated were of the following:
    - breakdown of title, content, and description sentiment mean
    """
    x = np.arange(len(df['source_name']))
    bar_width = 0.25

    plt.barh(x - bar_width, df['sentiment_mean'], height=bar_width, label='Sentiment Ttile Mean')
    plt.barh(x, df['sentiment_contents_mean'], height=bar_width, label='Sentiment Content Mean')
    plt.barh(x + bar_width, df['sentiment_description_mean'], height=bar_width, label='Sentiment Description Mean')

    plt.xlabel('Sentiment Values')
    plt.yticks(x, df['source_name'])  # Set y-ticks as source names
    plt.ylabel('Source Name')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), prop={'size': 9})
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_file', help='file path to processed and labelled dataset')
    parser.add_argument('-o', dest='output_file', help='file name of output')
    args = parser.parse_args()

    df = group_sentiment_by_newspaper(args.input_file)
    df = df[df['article_count'] >= 10]

    # output_fname = os.path.join(os.path.dirname('__file__'), args.output_file)
    # with open(output_fname, 'w') as f:
    #     json.dump(df.to_dict(), f, indent=4)
    
    # plotting the figures
    # top_sentiment_articles(args.input_file, args.output_file)
    plot_histogram(args.input_file)
    # plot_sentiment(df)
    # plot_sentiment_all(df)

    # print(df)