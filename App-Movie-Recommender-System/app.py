import pickle
import streamlit as st
import requests
import pandas as pd
import os

# -----------------------------
# PAGE CONFIG (FIRST LINE)
# -----------------------------
st.set_page_config(
    page_title="Movie Recommender System",
    layout="wide"
)

# -----------------------------
# BASE DIRECTORY
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MOVIE_DICT_PATH = os.path.join(BASE_DIR, "movie_dict.pkl")
SIMILARITY_PATH = os.path.join(BASE_DIR, "similarity.pkl")

TMDB_API_KEY = "df399de4718dd94d1fd24ecf1bfb230d"

# -----------------------------
# CACHE MODEL & DATA (BIG SPEED BOOST)
# -----------------------------
@st.cache_resource
def load_data():
    movie_dict = pickle.load(open(MOVIE_DICT_PATH, "rb"))
    movies = pd.DataFrame(movie_dict)
    similarity = pickle.load(open(SIMILARITY_PATH, "rb"))
    return movies, similarity


movies, similarity = load_data()

# -----------------------------
# CACHE POSTERS (NO REPEAT API CALLS)
# -----------------------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    except:
        pass

    return "https://via.placeholder.com/500x750?text=No+Poster"


# -----------------------------
# RECOMMENDATION LOGIC
# -----------------------------
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names, posters = [], []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


# -----------------------------
# UI
# -----------------------------
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Type or select a movie",
    movies["title"].values
)

if st.button("Show Recommendation"):
    with st.spinner("Finding best recommendations..."):
        names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
