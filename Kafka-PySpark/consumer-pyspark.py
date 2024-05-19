from pyspark.ml import PipelineModel
import re
import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
from kafka import KafkaConsumer
from json import loads
from pymongo import MongoClient
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Establish connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['bigdata_project'] 
collection = db['tweets'] 

# Download stopwords
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Assuming you have a SparkSession already created
spark = SparkSession.builder \
    .appName("classify tweets") \
    .getOrCreate()

# Load the model
pipeline = PipelineModel.load("logistic_regression_model.pkl")

def clean_text(text):
    if text is not None:
        # Remove links starting with https://, http://, www., or containing .com
        text = re.sub(r'https?://\S+|www\.\S+|\.com\S+|youtu\.be/\S+', '', text)
        
        # Remove words starting with # or @
        text = re.sub(r'(@|#)\w+', '', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove non-alphanumeric characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    else:
        return ''
    
class_index_mapping = { 0: "Negative", 1: "Positive", 2: "Neutral", 3: "Irrelevant" }

# Kafka Consumer
consumer = KafkaConsumer(
    'numtest',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    tweet = message.value[-1]  # get the Text from the list
    preprocessed_tweet = clean_text(tweet)
    # print("-> tweet : ", tweet)
    # print("-> preprocessed_tweet : ", preprocessed_tweet)
    # Create a DataFrame from the string
    data = [(preprocessed_tweet,),]  
    data = spark.createDataFrame(data, ["Text"])
    # Apply the pipeline to the new text
    processed_validation = pipeline.transform(data)
    prediction = processed_validation.collect()[0][6]

    print("-> Tweet:", tweet)
    print("-> preprocessed_tweet : ", preprocessed_tweet)
    print("-> Predicted Sentiment:", prediction)
    print("-> Predicted Sentiment classname:", class_index_mapping[int(prediction)])
    

    # Prepare document to insert into MongoDB
    tweet_doc = {
        "tweet": tweet,
        "prediction": class_index_mapping[int(prediction)]
    }

    # Insert document into MongoDB collection
    collection.insert_one(tweet_doc)

    print("/"*50)