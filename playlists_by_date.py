import spotipy
import argparse
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

# ./playlists_by_date.py 2020
# ^ Creates playlists up to 2020

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# User will give a date which is how far back they want to go
# Fetch saved tracks 50 at a time until the date is reached
# split the array based off of dates added, into half year chunks
# create playlists (if playlist with same name doesnt exist. except most recent in which case add more recent songs)

parser = argparse.ArgumentParser("playlists_by_date")
parser.add_argument("start_year", help="The year to start from when making playlists (inclusive)", type=int)
args = parser.parse_args()

final_year = args.start_year
if final_year < 1970 or final_year > datetime.now().year:
    print("Please provide a valid year between 1970 and the current year.")
    exit(1)

# Possible bug when len of results is 0
def split_tracks():
    print("Collecting tracks...")
    current_year = datetime.now().year
    current_half = 1 if datetime.now().month <= 6 else 2
    playlist_list = {}
    count = 0
    cont = True

    while cont:
        results = sp.current_user_saved_tracks(limit=50, offset=count)
        for idx, item in enumerate(results['items']):
            date_added = datetime.fromisoformat(item["added_at"][:-1])
            current_year = date_added.year
            current_half = 1 if date_added.month <= 6 else 2    
            # Break if reached the final year
            if (date_added.year < final_year):
                cont = False
                break
            # Add to appropriate playlist
            track = item['track']
            playlist_list.setdefault(f"{current_year} Vol. {current_half}", []).append(track['artists'][0]['name'] + " - " + track['name'])
        count += len(results['items'])
        if len(results['items']) == 0:
            break
    return playlist_list

def create_playlists(playlist_list):
    # Get all playlists 50 at a time
    # If name of playlist exists, mark in a new dictionary with same keys as playlist dict - default them to False and set to True if found
    # Create all not found playlists, and update all found playlists (? maybe)
    # if most recent playlist to create exists, then add any new songs to it
    playlist_exists = dict.fromkeys(playlist_list.keys(), False)
    count = 0
    while True:
        results = sp.current_user_playlists(limit=50, offset=count)
        for item in results['items']:
            print(item['name'])
            if item['name'] in playlist_exists:
                playlist_exists[item['name']] = True
        count += len(results['items'])
        if len(results['items']) == 0:
            break
    # For each playlist, either create and add tracks, or if existing compare tracks and add new ones
    return playlist_exists


playlists = split_tracks()
for playlist_name in playlists:
    print(playlist_name)
    for track in playlists[playlist_name]:
        print("   ", track)
for playlist_name in playlists:
    print(f"{playlist_name}: {len(playlists[playlist_name])} tracks")

playlist_exists = create_playlists(playlists)
for playlist_name in playlist_exists:
    if playlist_exists[playlist_name]:
        print(f"Playlist '{playlist_name}' exists and will be updated.")
    else:
        print(f"Playlist '{playlist_name}' does not exist and will be created.")


sp.playlist_add_items(playlist_id='37i9dQZF1DXcBWIGoYBM5M', items=['4iV5W9uYEdYUVa79Axb7Rh'])