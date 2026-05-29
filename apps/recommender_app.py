import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Force add project root to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from core.data_loader import load_tmdb_dataset
from core.preprocess import build_tags
from core.model import build_model, recommend
from core.tmdb_api import get_poster



st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

@st.cache_data
def load_data():
    df = load_tmdb_dataset()
    df = build_tags(df)
    return df

df = load_data()

@st.cache_resource
def load_model():
    return build_model(df)

tfidf, tfidf_matrix, model = load_model()

st.title("🎬 Modular Movie Recommendation System")
st.write("Search a movie and get recommendations with posters.")

movie_input = st.text_input("Enter a movie title:", placeholder="e.g., Avatar")
n_recs = st.slider("Number of recommendations", 3, 12, 6)

if movie_input:
    with st.spinner("Searching..."):
        found_title, results = recommend(movie_input, df, tfidf_matrix, model, n_recs)

    if found_title is None:
        st.error("❌ Movie not found.")
    else:
        st.success(f"✅ Movie found: **{found_title}**")
        st.image(get_poster(found_title), width=250)

        st.subheader("🎯 Recommended Movies")
        cols = st.columns(3)

        for i, title in enumerate(results):
            with cols[i % 3]:
                st.image(get_poster(title), width=200)
                st.caption(title)
