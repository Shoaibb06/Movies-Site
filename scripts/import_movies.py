import csv
import json
import requests
from datetime import datetime
from movies.models import *

base_url = 'https://api.themoviedb.org/3/'
api_key = '239cdc88309cbc455cf646b973534e4b'


def run():
    csv_file = open('tmdb_5000_movies.csv', encoding='utf8', mode='r')
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            budget = row['budget']
            genres = json.loads(row['genres'])
            for genre in genres:
                del genre['id']
            tmdb_id = row['id']
            language = row['original_language']
            overview = row['overview']
            release_date = row['release_date']
            release_date = datetime.strptime(release_date, '%m/%d/%Y') if release_date else datetime.strptime(
                '01/01/2010', '%m/%d/%Y')
            revenue = row['revenue']
            duration = int(row['runtime']) if row['runtime'].isdigit() else None
            status = row['status']
            tangline = row['tagline']
            title = row['title']
            url = f'{base_url}movie/{tmdb_id}?api_key={api_key}&language=en-US&page=1'
            movie_details = requests.get(url).json()
            # print(movie_details)
            if movie_details.keys().__contains__('belongs_to_collection') and str(
                    movie_details['belongs_to_collection']) != 'None' and str(
                movie_details['belongs_to_collection']['poster_path']) != 'None':

                poster_path = movie_details['belongs_to_collection']['poster_path']
            elif movie_details.keys().__contains__('poster_path') and str(
                    movie_details['poster_path']) != 'None':
                poster_path = movie_details['poster_path']
            else:
                poster_path = None

            url = f'{base_url}movie/{tmdb_id}/videos?api_key={api_key}&language=en-US&page=1'
            movie_details = requests.get(url).json()
            if movie_details.keys().__contains__('results'):
                for movie in movie_details['results']:
                    if movie['type'] == 'Trailer' and movie['site'] == 'YouTube' and movie['official']:
                        print(movie['type'] + '=>' + movie['site'])
                        video = movie['key']
                        break
                    elif movie['type'] == 'Trailer' and movie['site'] == 'YouTube':
                        print(movie['type'] + '=>' + movie['site'])
                        video = movie['key']
                        break
            movie = Movie(title=title, tagline=tangline, overview=overview, poster_url=poster_path,
                          language=language, status=status, budget=budget,
                          release_date=release_date, revenue=revenue, genres=genres, duration=duration, video=video)

            print(str(line_count) + str(movie) + str(poster_path))
            movie.save()
        line_count += 1
