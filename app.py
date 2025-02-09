import pickle
import streamlit as st
import requests

# Custom CSS to enhance the UI
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stSelectbox {
        background-color: light-gray;
        padding-left : 10px;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #ff4b4b;
        border-radius: 20px;
    }
    .movie-container {
        background-color: #262730;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .movie-title {
        font-weight: bold;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

@st.cache_data
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.title('Movie Recommender System')

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    " Type or select a movie from the dropdown",
    movie_list
)

if st.button('🚀 Show Recommendations'):
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    st.subheader(f"Top 5 recommendations for '{selected_movie}':")
    
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"""
            <div class="movie-container">
                <div class="movie-title">{recommended_movie_names[i]}</div>
                <img src="{recommended_movie_posters[i]}" width="100%">
            </div>
            """, unsafe_allow_html=True)

