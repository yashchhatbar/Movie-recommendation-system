import pickle
import pandas as pd
import requests
import time

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=df399de4718dd94d1fd24ecf1bfb230d&language=en-US"
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None
        except:
            time.sleep(1.5 * (attempt + 1))
    return None

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

poster_links = {}

for idx, row in movies.iterrows():
    movie_id = row['movie_id']
    poster = fetch_poster(movie_id)
    poster_links[movie_id] = poster
    print(f"[{idx}/{len(movies)}] Saved poster for movie_id={movie_id}")

# Save it to file
with open("poster_links.pkl", "wb") as f:
    pickle.dump(poster_links, f)

print("✅ All posters fetched and saved.")
