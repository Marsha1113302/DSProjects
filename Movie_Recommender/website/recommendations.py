import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
#from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix, save_npz, load_npz, hstack


# item_matrix = pd.read_csv('item_matrix3.csv',index_col = 'title')
moviesdf = pd.read_csv('moviesdf4.csv')
ui = csr_matrix(load_npz(r'C:\Users\marsh\Desktop\Capstone 3\website\user_item_matrix.npz'))
# ratingsdf = pd.read_csv('ratingsdf2.csv')

def recommended(favorites, non_favorites):
    newdf = pd.DataFrame(index = moviesdf.title)
    newdf['new_user_rating'] = np.nan
    newdf.loc[favorites,'new_user_rating'] = 5
    newdf.loc[non_favorites,'new_user_rating'] = 0
    scaler = StandardScaler()
    scaled = scaler.fit_transform(newdf)
    scaled = np.nan_to_num(scaled, nan=0)
    sparse_scaled = csr_matrix(scaled)
    ui_new = hstack([ui, sparse_scaled])
    U,S, Vt = svds(ui_new, k=50)
    Uk = U
    Sk = np.diag(S)
    Vk = Vt.T
    new_user_ratings = Uk @ Sk @ Vk[-1,:].T
    rec = pd.DataFrame(data= new_user_ratings, columns = ['rating'])
    rec['title'] = moviesdf.title
    rec = rec[~rec.title.isin(favorites)]
    rec = rec.sort_values('rating', ascending = False).head(10)
    rec = rec.merge(moviesdf, on = 'title',how ='inner')
    return rec

#def recommend(favorites,non_favorites):
#    newdf = pd.DataFrame(index = ui.index)
#    newdf['ratings'] = np.nan
#    newdf.loc[favorites, 'ratings'] = 5
#    newdf.loc[non_favorites,'ratings'] = 0
#    scaler = StandardScaler()
#    scaled = scaler.fit_transform(newdf)
#    scaled = np.nan_to_num(scaled, nan=0)
#    ui_new = np.hstack((ui, scaled))
#    im_cosine = cosine_similarity(ui_new)
#    np.fill_diagonal(im_cosine,0)
#    im = pd.DataFrame(im_cosine, index= ui.index, columns = ui.index)
#    recommendations_df = pd.DataFrame(columns = ['title','rating'])
#    for movie in moviesdf.index:
#        rating = (im[movie][favorites] * 5).sum() / im[movie].sum()
#        recommendations_df = recommendations_df.append({'title':movie, 'rating': rating}, ignore_index = True)
#    recommendations_df = recommendations_df.sort_values('rating', ascending = False)
#    return recommendations_df.merge(moviesdf, on = 'title', how= 'inner').head(10)