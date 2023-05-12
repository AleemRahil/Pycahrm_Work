import pprint
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = YOUR_SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = YOUR_SPOTIFY_CLIENT_SECRET

pp = pprint.PrettyPrinter(indent=4)

spotify_authenticator = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID, 
    client_secret=SPOTIFY_CLIENT_SECRET, 
    redirect_uri="http://example.com", 
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt"
    )
)

user_id = spotify_authenticator.current_user()["id"]



date_then = input(f"Tell me when do you want to travel in YYYY-MM-DD: ")
year = int(date_then[0:4])

# print(year)

billboard_response = requests.get(f"https://www.billboard.com/charts/hot-100/{date_then}/")
billboard_response.raise_for_status

soup=BeautifulSoup(billboard_response.content, "html.parser")


songs = soup.find_all(name="h3", id="title-of-a-story", class_="u-line-height-125")
song_titles = [title.getText().strip("\n\t") for title in songs]
artists = soup.find_all(name="span", class_="u-max-width-330")
artist_names = [name.getText().strip("\n\t") for name in artists]
song_and_artist = dict(zip(song_titles, artist_names))

# print(artist_names)
# print(song_titles)

song_uris=[]
for song_name in song_titles:    
    song_search_results = spotify_authenticator.search(q=f'track:{song_name}',type="track", limit=1)
    
    # pp.pprint(song_search_results)

    try:
        uri=song_search_results['tracks']['items'][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song_name} doesn't exist in Spotify. Skipped.")


playlist = spotify_authenticator.user_playlist_create(user=user_id, name=f"{date_then} Billboard 100", public=False, )

spotify_authenticator.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(f"New playlist '{date_then} Billboard 100' successfully created on Spotify!")