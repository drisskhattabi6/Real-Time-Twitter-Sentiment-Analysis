from django.shortcuts import render

from pymongo import MongoClient
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter
import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

# -----------------------------------------------------

# Connect to MongoDB server
client = MongoClient('mongodb://localhost:27017/')
# Select the database
db = client['bigdata_project']

# -----------------------------------------------------

def clean_text(text):
    # Remove URLs using regular expression
   text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
   # text = re.sub(r'\b(?:https?://|www\.)\S+\b', '', text)
   # Remove words starting with '@'
   text = re.sub(r'\b@\w+\b', '', text)
   # Remove non-alphanumeric characters
   text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
   # Convert text to lowercase
   text = text.lower()
   text = text.strip()
   return text

def preprocess_text(text):
    
    # clean the text
    text = clean_text(text)

    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Get English stopwords
    stop_words = set(stopwords.words('english'))
    
    # Remove stopwords
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    return filtered_tokens

class_list = ['Negative', 'Positive', 'Neutral', 'Irrelevant']

def plot_word_frequencies_per_class(data):
    keys_to_extract = ['tweet', 'prediction']
    result_tuples = [tuple(d[key] for key in keys_to_extract) for d in data]

    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'BigDataProject', 'static', 'imgs')

    all_words_per_class = {class_label: [] for class_label in class_list}
    color_map = {'Negative': 'red', 'Positive': 'blue', 'Neutral': 'green', 'Irrelevant': 'purple'}

    plt.figure(figsize=(12, 8))

    for tweet, prediction in result_tuples:
        class_texts = all_words_per_class[prediction]
        class_texts.extend(preprocess_text(tweet))

    for i, (class_label, class_words) in enumerate(all_words_per_class.items()):
        word_freq = Counter(class_words)
        top_words = dict(word_freq.most_common(5))
        df = pd.DataFrame(list(top_words.items()), columns=['Word', 'Frequency'])
        plt.bar(df['Word'] + f' ({class_label})', df['Frequency'], color=color_map[class_label], alpha=0.7, label=class_label)

    plt.xlabel('Words')
    plt.ylabel('Frequency')
    #  plt.title('Top Word Frequencies for Each Class')
    plt.legend()
    plt.xticks(rotation=70)
    plt.tight_layout()

    plot_path = os.path.join(static_folder, 'Word_Frequencies_for_all_classes.png')
    plt.savefig(plot_path)

# -----------------------------------------------------

def dashboard(request):
   data = list(db.tweets.find())  # Fetch all data from MongoDB

   len_data = len(data)
   print("len_data : ", len_data)

   if len_data == 0:
      context = {'len_data': len_data}
      return render(request, 'dashboard/index.html',context)
   
   sentiment_counts = {label: 0 for label in ['Negative', 'Positive', 'Neutral', 'Irrelevant']}
   for entry in data:
      sentiment_counts[entry['prediction']] += 1


   # Calculate the rate of each class
   sentiment_rates = {label: round((count / len_data) * 100, 2)  for label, count in sentiment_counts.items()}

   # pie_plot(sentiment_counts)
   # bar_plot(sentiment_counts)
   # plot_word_frequencies_per_class(data)
   plot_word_frequencies_per_class(data)

   context = {
      'data': data,
      'len_data': len_data,
      'sentiment_rates': sentiment_rates,
      'sentiment_counts': sentiment_counts,
   }
   return render(request, 'dashboard/index.html', context)


def classify(request) :
    
   error = False
   error_text = ""
   prediction = ""
   text = ""

   if request.method == 'POST':

      text = request.POST.get('text')

      if len(text.strip()) > 0 :
         from .consumer_user import classify_text
         prediction = classify_text(text)
      
      else : 
         error_text = "the Text is empty!! PLZ Enter Your Text."

   context = {
      "error" : error,
      "error_text" : error_text,
      "prediction" : prediction,
      "text" : text
   }
   return render(request, 'dashboard/classify.html', context)

