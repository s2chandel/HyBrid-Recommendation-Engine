
import pandas as pd
import numpy as np
import pymssql
import pickle
from sklearn.preprocessing import normalize
from sklearn.preprocessing import LabelEncoder 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score


indices = pickle.load(open("../helper/indices.pkl","rb"))
Data = pickle.load(open("../helper/Data.pkl","rb"))

def live_recommendations(article_id=None):
    idx = Data.index[Data['ArticleId'] == article_id]
    lst = []
    for a_id in indices[idx][:]:
        idx = list(Data.iloc[a_id]['ArticleId'][1:6])

    return idx


"""
Top Rated:
Collaborative Filtering
"""
articles_views = pd.read_sql_query('''SELECT* FROM dbo.ArticleViews''', conn)
views = articles_views[['UserId','ArticleId']]
rating_articleId = views['ArticleId']
rating_userId = views['UserId']
ratings_df = views.groupby(['UserId','ArticleId']).size().reset_index(name='Views_ratings')
ratings = ratings_df[['UserId', 'ArticleId', 'Views_ratings']]
ratings['Views_ratings'] = (ratings['Views_ratings']-ratings['Views_ratings'].mean())/ratings['Views_ratings'].std()
"""
loading top_n
"""

top_n = pickle.load(open("../helper/top_n.pkl","rb"))

def top_recommended_user_interests(user_id=None):

    articles = top_n[user_id]
    df = pd.DataFrame(articles,columns=['article_id','value'])
    result = df['article_id'].astype(int)

    return list(result)

"""recommend top 5 results for cold users"""
def top_rated():
    most_viewed = ratings.sort_values(by='Views_ratings',ascending=False)
    top_rated = most_viewed.drop_duplicates(subset=['ArticleId'],keep='first')
    top_rated = top_rated['ArticleId'][:5]
    top_rated = top_rated.astype(int)
    return list(top_rated)


"""final recommendations"""
def final_recommendations(user,article_id):
    print({"UserId":user,"ArticleId":article_id})
    if article_id:
        idx_article = Data['ArticleId'].unique()
        if article_id in idx_article:
            article_based = live_recommendations(article_id)
        else:
            article_based = []

    if user:
        idx = ratings_df['UserId'].unique()

        if user in idx:
            response = top_recommended_user_interests(user)
        else:
            response = []
    return {"live_recommendations":article_based,
    "top_recommended_user_interests":response,
    "top_rated":top_rated()}

 response = top_recommended_user_interests(user)
#         else:
#             response = []
#     return {"live_recommendations":article_based,
#     "top_recommended_user_interests":response,
#     "top_rated":top_rated_en_gb()}
# """