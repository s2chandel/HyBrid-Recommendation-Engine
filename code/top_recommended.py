import pandas as pd
import numpy as np
from collections import defaultdict
import surprise
from surprise import SVD
from surprise import Dataset
import pymssql
import pickle

# sql_connection

"""
data preprocessing
"""
articles_views = pd.read_sql_query('''SELECT* FROM dbo.ArticleViews''', conn)

views = articles_views[['ArticleId','UserId']]

# slicing data points on basis of country and language
views = views[['UserId','ArticleId']]
ratings_df = views.groupby(['UserId','ArticleId']).size().reset_index(name='Views_ratings')
ratings = ratings_df[['UserId', 'ArticleId', 'Views_ratings']]
ratings['Views_ratings'] = (ratings['Views_ratings']-ratings['Views_ratings'].mean())/ratings['Views_ratings'].std()
feature_sparse_mat = ratings.pivot(index='UserId', columns='ArticleId', values='Views_ratings')

# ratings scale
lower_ratings = ratings['Views_ratings'].min()
high_ratings = ratings['Views_ratings'].max()

reader = surprise.Reader(rating_scale=(-0.32,151.50))


data = surprise.Dataset.load_from_df(ratings,reader)
trainset = data.build_full_trainset()
algo = SVD()
algo.fit(trainset)


# predict ratings for all users
testset = trainset.build_anti_testset()
predictions = algo.test(testset)

def top_recommended_user_interests(predictions, n=5):
    """top 5 recommended articles for each user"""
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

top_n = top_recommended_user_interests(predictions,n=5)
"""
serailising model
"""
pickle.dump(top_n open("../helper/top_n.pkl", "wb"))
