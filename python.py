import requests
import pandas as pd

API_KEY = 'ENTER YOUR READ API KEY HERE'
BASE_URL = 'https://api.themoviedb.org/3'
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json;charset=utf-8'
}

data = []
page_number = 1
movies_collected = 0

while movies_collected < 1250:
    # Fetch top-rated movies for the current page
    response = requests.get(f'{BASE_URL}/movie/top_rated?page={page_number}', headers=HEADERS)

    # Check if the response status is OK
    if response.status_code != 200:
        raise Exception(f"Error fetching top-rated movies. Status code: {response.status_code}\n{response.text}")

    # Check if 'results' is in the response content
    if 'results' not in response.json():
        raise Exception("Unexpected response format. 'results' key not found.\n" + str(response.json()))

    movies = response.json()['results']

    for movie in movies:
        movie_id = movie['id']
        movie_title = movie['title']

        # Fetch cast for this movie
        response = requests.get(f'{BASE_URL}/movie/{movie_id}/credits', headers=HEADERS)
        
        # Check if the response status is OK
        if response.status_code != 200:
            print(f"Error fetching cast for movie {movie_title}. Status code: {response.status_code}")
            print(response.text)
            continue  # Skip this movie and move to the next

        cast = response.json()['cast']

        for actor in cast:
            data.append([movie_title, actor['name']])
        
        movies_collected += 1
        if movies_collected >= 1250:
            break

    page_number += 1

# Convert the data list to a pandas dataframe and return
df = pd.DataFrame(data, columns=['Movie Title', 'Actor Name'])
df
