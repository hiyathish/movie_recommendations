import pandas as pd
import ast

def load_tmdb_dataset():
    movies = pd.read_csv("../data/tmdb_5000_movies.csv")
    credits = pd.read_csv("../data/tmdb_5000_credits.csv")

    # Convert JSON-like strings
    movies["genres"] = movies["genres"].apply(lambda x: [d["name"] for d in ast.literal_eval(x)])
    movies["keywords"] = movies["keywords"].apply(lambda x: [d["name"] for d in ast.literal_eval(x)])

    credits["cast"] = credits["cast"].apply(lambda x: [d["name"] for d in ast.literal_eval(x)])
    credits["crew"] = credits["crew"].apply(lambda x: [d["job"] + ": " + d["name"] for d in ast.literal_eval(x)])

    # Merge
    movies = movies.merge(credits, left_on="id", right_on="movie_id", how="left")

    # FIX: Ensure a clean title column exists
    if "title" not in movies.columns:
        if "original_title" in movies.columns:
            movies["title"] = movies["original_title"]
        elif "title_x" in movies.columns:
            movies["title"] = movies["title_x"]
        elif "title_y" in movies.columns:
            movies["title"] = movies["title_y"]
        else:
            raise ValueError("No usable title column found in dataset.")

    return movies
