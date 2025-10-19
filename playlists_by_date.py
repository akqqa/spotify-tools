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

def split_tracks():
    current_year = datetime.now().year
    current_half = 1 if datetime.now().month <= 6 else 2
    current_list = []
    playlist_list = {}
    count = 0
    cont = True

    while cont:
        results = sp.current_user_saved_tracks(limit=50, offset=count)
        print("calling")
        for idx, item in enumerate(results['items']):
            playlist_found = False
            print("iterating")
            while not playlist_found:
                date_added = datetime.fromisoformat(item["added_at"][:-1])
                print(date_added)
                half = 1 if date_added.month <= 6 else 2
                if (date_added.year != current_year or half != current_half):
                    # Put current list into dictionary and start new list
                    playlist_name = f"{current_year} Vol. {current_half}"
                    playlist_list[playlist_name] = current_list
                    current_list = []
                    if (current_half == 2):
                        current_half = 1
                    else:
                        current_half = 2
                        current_year -= 1
                    continue # Starts again with new playlist
                playlist_found = True
                track = item['track']
                print(idx, track['artists'][0]['name'], " – ", track['name'])
                print("current_year:", current_year, "current_half:", current_half)
                count += 1
            if (date_added.year < final_year):
                cont = False
                break
            # Added to current list
            current_list.append(track['artists'][0]['name'])
    return playlist_list

playlists = split_tracks()

#print playlists
for playlist_name in playlists:
    print(playlist_name)
    for track in playlists[playlist_name]:
        print("   ", track)
for playlist_name in playlists:
    print(f"{playlist_name}: {len(playlists[playlist_name])} tracks")