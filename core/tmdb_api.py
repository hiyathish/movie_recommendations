import requests

TMDB_API_KEY = "e2a12085118c4927f382043d293d76fc"
TMDB_READ_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9..."

HEADERS = {
    "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
    "Content-Type": "application/json;charset=utf-8",
}

def get_poster(title):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"query": title, "api_key": TMDB_API_KEY}

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        data = response.json()
        results = data.get("results", [])
        if results:
            poster_path = results[0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass

    return "https://via.placeholder.com/300x450?text=No+Image"
