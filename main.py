import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# User will give a date which is how far back they want to go
# Fetch saved tracks 50 at a time until the date is reached
# split the array based off of dates added, into half year chunks
# create playlists (if playlist with same name doesnt exist. except most recent in which case add more recent songs)

results = sp.current_user_saved_tracks(limit=50)
for idx, item in enumerate(results['items']):
    print(item["added_at"])
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])