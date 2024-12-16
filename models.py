from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

if (torch.cuda.is_available()):
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

# TODO
# Write a model, or multiples models, that analyzes the sentiment of an articles and 
# returns the sentiment of it. The sentiment should be an integer between -1 and 1, 
# where -1 represents negative sentiment and 1 positive sentiment

def sentiment_analyzer(X):
    """
    Analyze the sentiment of a given text and return a sentiment score.

    The function takes a string input and evaluates the sentiment expressed in the text.
    It returns a sentiment score that ranges from -1 to 1, where:
      -1 indicates extremely negative sentiment,
       0 indicates neutral sentiment, and
       1 indicates extremely positive sentiment.

    Args:
        text (str): The text to be analyzed for sentiment.

    Returns:
        float: A sentiment score between -1 and 1.
    
    Example:
        >>> sentiment_analyzer("I love sunny days.")
        0.8
        
        >>> sentiment_analyzer("I hate getting stuck in traffic.")
        -0.7
    """
    # check if all elements in X are strings        
    X = [str(item) for item in X]
    
    # load the model
    model = AutoModelForSequenceClassification.from_pretrained('distilbert/distilbert-base-uncased-finetuned-sst-2-english')
    tokenizer = AutoTokenizer.from_pretrained('distilbert/distilbert-base-uncased-finetuned-sst-2-english')

    # move to device
    model = model.to(device)

    # predict the sentiment of the text in batches
    batch_size = 8
    all_predictions = []

    for i in range(0, len(X), batch_size):
        batch_texts = X[i:i + batch_size]
        batch = tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model(**batch)
            
            batch_predictions = F.softmax(outputs.logits, dim=1)
            all_predictions.append(batch_predictions)
    
    # concatenate the predictions
    all_predictions = torch.cat(all_predictions, dim=0)
    labels = torch.argmax(all_predictions, dim=1).tolist()
    # Get the maximum probability for each prediction
    scores = torch.max(all_predictions, dim=1).values.tolist()

    # Convert scores to negative if label is 0 (negative sentiment)
    scores = [-score if label == 0 else score for score, label in zip(scores, labels)]


    return scores

    