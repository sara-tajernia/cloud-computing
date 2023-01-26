import pyspark
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator


# load data
data = pd.read_csv('ratings.csv') 
matrix = data
matrix

# create spark session
spark = pyspark.sql.SparkSession.builder.getOrCreate()
spark

# create spark dataframe with header and infer schema
# read our data from ratings.csv
# header -> Record For Column Names 
# inferSchema -> automatically infers column types based on the data
df = spark.read.csv('ratings.csv', header=True, inferSchema=True)
df.show()

# cast all the columns to int
df = df.select(df.game_id.cast('int'), df.user_id.cast('int'), df.rating.cast('int'))
df

# build test and train data
# 80% training & 20% testing
# Calling the function with the same seed will always generate the same results
(train, test) = df.randomSplit([0.8, 0.2], seed = 21)


# build the recommendation model using ALS on the training data
# maxIter -> maximum number of iterations to run
# regParam -> regularization parameter in ALS
als = ALS(maxIter=5, regParam=0.01, userCol='user_id', itemCol='game_id', ratingCol='rating')

# fit the model to the training data
model = als.fit(df)
# model = als.fit(train)

# evaluate the model by computing the RMSE on the test data
# evaluate the model by computing the RMSE on the test data
# algorithm which can transform one DataFrame into another DataFrame
predictions = model.transform(test)
predictions.show()
# size of predictions


evaluator = RegressionEvaluator(metricName='rmse', labelCol='rating', predictionCol='prediction')

# # get the RMSE
# rmse = evaluator.evaluate(predictions)
# print('Root-mean-square error = ' + str(rmse))

# get input user id
user_id = int(input('Enter user id: '))



# Generate top 5 movie recommendations for each user
userRecs = model.recommendForAllUsers(5)
userRecs.show()

print('userRecs')

# show userRecs with user_id with prediction score
userRecs.filter(userRecs['user_id']==user_id).show()
userRecs.filter(userRecs['user_id']==user_id).select('recommendations').show()
recom_list = userRecs.filter(userRecs['user_id']==user_id).select('recommendations').collect()


# print name game with game_id
games = pd.read_csv('games.csv')
for i in range(len(recom_list[0][0])):
    game_data = games.loc[games['game_id'] == recom_list[0][0][i][0]]
    print(i+1 , ':', 'game:' ,game_data['name'].values[0], 'score:', recom_list[0][0][i][1])