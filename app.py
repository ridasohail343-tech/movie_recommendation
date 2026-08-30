import os
import pickle
import difflib

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB") or os.getenv("TMDB_API_KEY")

with open("movies.pkl", "rb") as movie_file:
    movies = pickle.load(movie_file)

with open("similarity.pkl", "rb") as similarity_file:
    similarity = pickle.load(similarity_file)


def fetch_poster(movie_id):
    if not TMDB_API_KEY:
        return "https://via.placeholder.com/500x750?text=TMDB+API+Key+Missing"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except requests.RequestException:
        pass

    return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    all_titles = movies["original_title"].tolist()
    close_matches = difflib.get_close_matches(movie, all_titles, n=1, cutoff=0.3)

    if not close_matches:
        return [], []

    matched_title = close_matches[0]
    movie_index = movies[movies["original_title"] == matched_title].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]]["id"]
        recommended_titles.append(movies.iloc[i[0]]["original_title"])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters


st.title("Movie Recommendation System")
st.write("Find movies similar to your favorite movie.")

if not TMDB_API_KEY:
    st.warning("TMDB API key is missing. Add it to your .env file as TMDB or TMDB_API_KEY.")

selected_movie = st.selectbox("Select a movie", movies["original_title"].values)

if st.button("Recommend"):
    titles, posters = recommend(selected_movie)

    if titles:
        st.subheader("Recommended Movies")
        cols = st.columns(5)
        for idx in range(len(titles)):
            with cols[idx]:
                st.image(posters[idx])
                st.write(titles[idx])
    else:
        st.error("Movie not found.")