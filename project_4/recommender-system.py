import pyspark
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator


# # load data
# data = pd.read_csv('ratings.csv') 
# games = pd.read_csv('games.csv')

# matrix = data
# matrix

spark = pyspark.sql.SparkSession.builder.appName('Games').getOrCreate()
# spark

# create spark dataframe with header and infer schema
df = spark.read.csv('ratings.csv', header=True, inferSchema=True)

# cast all the columns to int
df = df.select(df.user_id.cast('int'), df.game_id.cast('int'), df.rating.cast('int'))

# build test and train data
(train, test) = df.randomSplit([0.8, 0.2], seed = 40)



# build the recommendation model using ALS on the training data
als = ALS(maxIter=5, regParam=0.01, userCol='user_id', itemCol='game_id', ratingCol='rating')

# fit the model to the training data
model = als.fit(train)

# evaluate the model by computing the RMSE on the test data
predictions = model.transform(test)
evaluator = RegressionEvaluator(metricName='rmse', labelCol='rating', predictionCol='prediction')

# get the RMSE
rmse = evaluator.evaluate(predictions)
print('Root-mean-square error = ' + str(rmse))