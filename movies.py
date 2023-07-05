import requests
import pandas as pd
import time

def get_marvel_movie_ids(api_key):
    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        'api_key': api_key,
        'query': 'Marvel Studios',  # Search for movies that include 'Marvel' in the title or description
        'language': 'en-US',
        'page': 1  # Start at the first page of results
    }

    while True:
        response = requests.get(url, params=params)
        data = response.json()

        for movie in data['results']:
            # Check if the movie was released in or after the year 2000
            if movie['release_date'][:4]  <= '2023' >= '2000':
                if 'Marvel Studios Assembled: The Making of' not in movie['title']:
                        movie_ids.append(movie['id'])
        if data['page'] >= data['total_pages']:
            # If we've reached the last page of results, stop the loop
            break
        else:
            # Otherwise, move on to the next page of results
            params['page'] += 1

        # Wait for 0.25 second to avoid hitting the rate limit
        time.sleep(0.25)

    return movie_ids
def get_movie_data(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits"

    response = requests.get(url)
    data = response.json()
    if data['budget'] > 0 and data['revenue'] > 0:

        # Get the director and main actors
        director = ''
        actors = []
        for person in data['credits']['crew']:
            if person['job'] == 'Director':
                director = person['name']
        for person in data['credits']['cast']:
            actors.append(person['name'])
        # Limit to the top 5 actors
        actors = actors[:5]

        movie_data = {
            'Title': data['title'],
            'Release Year': data['release_date'][:4],  # get the year from the release date
            'Rating': data['vote_average'],
            'Director': director,
            'Main Actors': ', '.join(actors),  # join the actor names into a single string
            'Budget': data['budget'],
            'Box Office Earnings': data['revenue'],
        }

        return movie_data
    else:
        return None
api_key = '69f9311b7c760fdb7afcf923ceef94c3'
movie_ids = []
get_marvel_movie_ids(api_key)


# Create an empty DataFrame to store the movie data
df = pd.DataFrame()
for movie_id in movie_ids:
    try:
        movie_data = get_movie_data(movie_id, api_key)
        if movie_data is not None:  # Only append if the movie data is not None
            df = pd.concat([df, pd.DataFrame([movie_data])])
            print(f"Collected data for movie ID {movie_id}")
        else:
            print(f"Skipped movie ID {movie_id} due to zero budget")
    except Exception as e:
        print(f"Failed to collect data for movie ID {movie_id}: {e}")
# Save the DataFrame to a CSV file
df.to_csv('movies.csv', index=False)