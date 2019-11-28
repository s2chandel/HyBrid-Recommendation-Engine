import pandas as pd
import pickle
import pymssql
from sklearn.neighbors import NearestNeighbors

# sql_connection

# GB_Data
articles_fav = pd.read_sql_query('''SELECT* FROM dbo.ArticleFavorites''', conn)
articles_category = pd.read_sql_query('''SELECT* FROM dbo.ArticleCategory''', conn)
articles = pd.read_sql_query('''SELECT Id,Title,Content,Slug,Status FROM dbo.Articles''', conn)
articles_ref = pd.read_sql_query('''SELECT* FROM dbo.ArticleReferences''', conn)
categories = pd.read_sql_query('''SELECT* FROM dbo.Categories''', conn)
articles_views = pd.read_sql_query('''SELECT* FROM dbo.ArticleViews''', conn)

# Preprocessing
article_data = pd.merge(articles_category,categories,left_on='CategoryId',right_on='Id')
Data = pd.merge(articles,article_data,left_on='Id',right_on='ArticleId')
Data = Data[['ArticleId','Title_x','Content','Title_y']]
Data.columns =['ArticleId','Title','Content','Category']
Data = Data.drop_duplicates(subset=['ArticleId'],keep='first')
Data_en_gb =  Data.reset_index(drop=True)

"""
NearestNeighbors(Unsupervised Learning)
"""
# feature matrix
articleId = Data['ArticleId']
features = Data[['Title', 'Content', 'Category']]
features = pd.get_dummies(features)
features = features.reset_index(drop=True)

# NearestNeighbors

nn = NearestNeighbors(n_neighbors=6,algorithm='ball_tree')#n_neighbors=no.of data points(nearest neighbors) your model wants to consider
nbrs = nn.fit(features)
distance , indices = nbrs.kneighbors(features)

"""
indices dump from clustering model
"""

pickle.dump(indices,open("../helper/indices.pkl","wb"))

"""
preprocessed data dump
"""
pickle.dump(Data, open("../helper/Data.pkl","wb"))