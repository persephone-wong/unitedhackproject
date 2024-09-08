from django.shortcuts import redirect
from spotipy import SpotifyOAuth

def spotify_auth(request):
    sp_oauth = SpotifyOAuth(client_id='',
                            client_secret='',
                            redirect_uri='http://localhost:8000/spotify_callback/',
                            scope='user-read-playback-state user-modify-playback-state')
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)