from newsapi import NewsApiClient
import requests
import json
import csv
import pandas as pd

# Getting data of a comapny for the last month using api and storting it into a json file

url = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'domains=bloomberg.com&'
       'searchIn=Title&'
       'language=en&'
       'from=2022-08-20&'
       'sortBy=publishedAt&'
       'apiKey=6d82ec14ce134588855d9997766efd9c')

response = requests.get(url)

with open("data.json", "w") as outfile:
    json.dump(response.json(), outfile)

# Converting JSON Data into CSV file

with open("data.json","r") as data_file:
    data = json.load(data_file)
 
news_data = data['articles']

data_file = open('data_file.csv', 'w')

csv_writer = csv.writer(data_file)
 
count = 0
for news in news_data:
    if count == 0:
 
        header = news.keys()
        csv_writer.writerow(header)
        count += 1
 
    csv_writer.writerow(news.values())
 
data_file.close()

# Checking encoding of the dataset

with open('data_file.csv') as f:
    print(f)

# Cleaning the dataset
# Dropping Coloumns

df = pd.read_csv('data_file.csv', encoding='cp1252')
df.drop('source', inplace=True, axis=1)
df.drop('url', inplace=True, axis=1)
df.drop('urlToImage', inplace=True, axis=1)
df.drop('publishedAt', inplace=True, axis=1)

# Renaming 1st Coloumn

df.index.name = "id"

# Combining descrption and content coloumns

df["text"] = df["description"].str.cat(df["content"], sep = "-")

# Dropping description and content coloumns

df.drop('description', inplace=True, axis=1)
df.drop('content', inplace=True, axis=1)
df = df.drop_duplicates()

# Saving it into cleaner csv file

df.to_csv('clean_data_file.csv')

# Checking shape of the new dataset

df1 = pd.read_csv('clean_data_file.csv', encoding='cp1252')

print("Shape of News data:", df1.shape)
print("News data columns", df1.columns)
