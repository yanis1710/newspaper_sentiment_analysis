from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

if (torch.cuda.is_available()):
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

MODEL = "classla/xlm-r-parlasent"

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
    X = [str(item) for item in X]
    
    # load the model
    model = AutoModelForSequenceClassification.from_pretrained(MODEL).to(device)
    tokenizer = AutoTokenizer.from_pretrained(MODEL)

    # predict the sentiment of the text in batches for less memory usage
    batch_size = 8
    all_predictions = []

    for i in range(0, len(X), batch_size):
        batch_texts = X[i:i + batch_size]
        batch = tokenizer(batch_texts, padding=True, truncation=True, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model(**batch)
            
            batch_predictions = outputs.logits
            all_predictions.append(batch_predictions)
    
    # concatenate the predictions
    all_predictions = torch.cat(all_predictions, dim=0)
    # print(max(all_predictions))
    # print(min(all_predictions))

    # map predictions from [0, 6] range to [-1, 1] range using linear scaling
    # originally 2 * all_predictions / 6 - 1
    all_predictions = all_predictions / 3 - 1
    # clip predictions to be between -1 and 1
    all_predictions = torch.clip(all_predictions, -1, 1)
    # print(max(all_predictions))
    # print(min(all_predictions))

    predictions = [pred[0] for pred in all_predictions.tolist()]
    return predictions
