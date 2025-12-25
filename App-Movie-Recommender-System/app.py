import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=df399de4718dd94d1fd24ecf1bfb230d&language=en-US'
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # raises HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', "")

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return "https://via.placeholder.com/500x750?text=No+Poster"  # fallback image


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters

# Load Data
movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    for i in range(5):
        with columns[i]:
            st.text(names[i])
            st.image(posters[i])