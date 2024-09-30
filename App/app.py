import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    try:
        api_key = "8265bd1679663a7ea12ac168da84d2e8"
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
        response = requests.get(url, timeout=0.3)
        data = response.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again later.")


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommend_movies = []
    recommend_movies_posters = []
    for movie in movies_list:
        recommend_movies.append(movies['title'][movie[0]])
        recommend_movies_posters.append(fetch_poster(movies['movie_id'][movie[0]]))
    return recommend_movies, recommend_movies_posters


st.title('Movie Recommender System')

st.write("")

movies = pickle.load(open('data/movies_pkl', 'rb'))
similarity = pickle.load(open('data/similarity_pkl', 'rb'))

selected_movie_name = st.selectbox("Select a Movie", movies['title'].values)

st.write("")

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    st.subheader("Top 10 Recommended Movies:")
    for row in range(0, 10, 5):
        cols = st.columns(5)
        for col, index in zip(cols, range(row, row + 5)):
            if index < len(names):
                with col:
                    if posters[index] is not None:
                        st.image(posters[index])
                    st.write(names[index])