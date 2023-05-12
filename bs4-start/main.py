from bs4 import BeautifulSoup
import requests

URL = 'https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/'

response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')
all_movies = soup.find_all(name="h3", class_="title")
movie_titles = [movie.getText() for movie in all_movies]
movie_list=movie_titles[::-1]

with open("movies.txt", mode="w") as file:
    for movie in movie_list:
        file.write(f"{movie}\n")
