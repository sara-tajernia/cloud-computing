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

# get input user id
user_id = int(input('Enter user id: '))

# make a single prediction
single_user = test.filter(test['user_id']==user_id).select(['user_id', 'game_id'])
print('single_user')
single_user.show()

# recommend top 5 games for the user
recommendations = model.transform(single_user)
print('recommendations')
recommendations.orderBy('prediction', ascending=False).show(n=5)


# list of game_id recommended to user 
game_id = recommendations.orderBy('prediction', ascending=False).select('game_id').collect()
recomendation_score = recommendations.orderBy('prediction', ascending=False).select('prediction').collect()


games = pd.read_csv('games.csv')

# print name game with game_id
for i in range(len(game_id)):
    game_data = games.loc[games['game_id'] == game_id[i][0]]
    print(i+1 , ':', 'game:' ,game_data['name'].values[0], '  score:', recomendation_score[i][0])