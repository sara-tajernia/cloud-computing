# Data processing
import pandas as pd
import numpy as np
import scipy.stats
# Visualization
import seaborn as sns
# Similarity
from sklearn.metrics.pairwise import cosine_similarity
import os


data = pd.read_csv('ratings_t.csv')
games = pd.read_csv('games_t.csv')

# drop columns of release data, summery and meta score
games.drop(games.columns[[2,3,4]], axis=1, inplace=True)

# merge data matching game_id 
merged_data = pd.merge(data, games, on='game_id')

# create matrix row->game_id, column->user_id, value->rating
matrix = merged_data.pivot_table(index='game_id', columns='user_id', values='rating')

# save matrix to file using numpy
# np.save('matrix.npy', matrix)

# read matrix from file 
# matrix = np.load('matrix.npy')

# # normalize data
# Normalize user-item matrix
matrix_norm = matrix.subtract(matrix.mean(axis=1), axis = 'rows')
matrix_norm.head()