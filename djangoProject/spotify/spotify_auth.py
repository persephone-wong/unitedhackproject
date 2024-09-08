from django.shortcuts import redirect
from spotipy import SpotifyOAuth
import os

def spotify_auth(request):

    sp_oauth = SpotifyOAuth( client_id = os.getenv('SPOTIFY_CLIENT_ID'),
                            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET'),
                            redirect_uri='http://localhost:8000/spotify_callback/',
                            scope='user-read-playback-state user-modify-playback-state')
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)