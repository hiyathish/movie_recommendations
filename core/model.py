from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

def build_model(df):
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["tags"])

    model = NearestNeighbors(metric="cosine", algorithm="brute")
    model.fit(tfidf_matrix)

    return tfidf, tfidf_matrix, model


def recommend(movie_name, df, tfidf_matrix, model, n_recs=8):
    movie_name = movie_name.lower().strip()

    idx = df[df["title"].str.lower() == movie_name].index

    if len(idx) == 0:
        partial = df[df["title"].str.lower().str.contains(movie_name)]
        if partial.empty:
            return None, None
        found_title = partial.iloc[0]["title"]
        idx = [partial.index[0]]
    else:
        found_title = df.iloc[idx[0]]["title"]

    idx = idx[0]
    distances, indices = model.kneighbors(tfidf_matrix[idx], n_neighbors=n_recs)

    results = []
    for i in range(1, len(indices[0])):
        movie_idx = indices[0][i]
        results.append(df.iloc[movie_idx]["title"])

    return found_title, results
