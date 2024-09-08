from django.shortcuts import render, redirect
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

def spotify_callback(request):
    sp_oauth = SpotifyOAuth(client_id='',
                            client_secret='',
                            redirect_uri='http://localhost:8000/',)
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    request.session['token_info'] = token_info
    return redirect('/')

def spotify_playlist(request):
    token_info = request.session.get('token_info', None)
    if not token_info:
        return redirect('spotify_auth')

    sp = Spotify(auth=token_info['access_token'])
    playlists = sp.current_user_playlists()
    context = {
        'playlists': playlists['items']
    }
    return render(request, 'spotify.html', context)