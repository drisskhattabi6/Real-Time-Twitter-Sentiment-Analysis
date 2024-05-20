from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# from pymongo import MongoClient

# import os
# print(" the model is exist : ", os.path.exists("logistic_regression_model.pkl"))

# Establish connection to MongoDB
# client = MongoClient('localhost', 27017)
# db = client['bigdata_project'] 
# collection = db['tweets'] 

# Assuming you have a SparkSession already created
spark = SparkSession.builder \
    .appName("classify tweets") \
    .getOrCreate()

# import os
# print(" the model is exist : ", os.path.exists("../logistic_regression_model.pkl"))

# Load the model
pipeline = PipelineModel.load("logistic_regression_model.pkl")

def clean_text(text):
    if text is not None:
        # Remove links starting with https://, http://, www., or containing .com
        text = re.sub(r'https?://\S+|www\.\S+|S+\.com\S+|youtu\.be/\S+', '', text)
        
        # Remove words starting with # or @
        text = re.sub(r'(@|#)\w+', '', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove non-alphabitic characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    else:
        return ''
    
class_index_mapping = { 0: "Negative", 1: "Positive", 2: "Neutral", 3: "Irrelevant" }


def classify_text(text: str) :
    preprocessed_tweet = clean_text(text)
    data = [(preprocessed_tweet,),]  
    data = spark.createDataFrame(data, ["Text"])
    # Apply the pipeline to the new text
    processed_validation = pipeline.transform(data)
    prediction = processed_validation.collect()[0][6]

    print("-> Tweet : ", text)
    print("-> preprocessed_tweet : ", preprocessed_tweet)
    print("-> Predicted Sentiment : ", prediction)
    print("-> Predicted Sentiment classname : ", class_index_mapping[int(prediction)])
    

    # # Prepare document to insert into MongoDB
    # tweet_doc = {
    #     "tweet": text,
    #     "prediction": class_index_mapping[int(prediction)]
    # }

    # # Insert document into MongoDB collection
    # collection.insert_one(tweet_doc)

    print("/"*50)

    return class_index_mapping[int(prediction)]

# print("/"*50)