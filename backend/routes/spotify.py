from flask import Blueprint, request, session
from urllib.parse import urlencode, quote
from utils.spotify import get_auth_code_obj, get_token_header, get_expired_date, check_authentication, extract_track, get_track_hash
from functools import wraps
import os
import requests

auth_app = Blueprint('auth', __name__)

def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if check_authentication(session) is None:
            return {'status': 401, 'message': 'Not authorized to view resource'}, 401
        else:
            return f(*args, **kwargs)
    return decorated_function

@auth_app.route('/auth', methods=["GET", "POST"])
def spotify_auth():
    if session.get('spotify_code') is None:
        redirect_url = os.getenv('APP_BASE_URL')+'/spotify/auth/callback/'
        query_parameters = {
            'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
            'response_type': 'code',
            'redirect_uri': redirect_url,
            'scope': 'playlist-modify-public playlist-modify-private playlist-read-collaborative playlist-read-private',
        }
        spotify_url = 'https://accounts.spotify.com/authorize?' + urlencode(query_parameters)
        return {'status':200, 'message': spotify_url}
    else:
        d = {'status': 200, 'message': 'Already authenticated'}
        return d, 200

@auth_app.route('/auth/callback/', methods=["GET"])
def spotify_callback():
    d = {
        'status': 200,
        'message': 'Logged into spotify successfully.'
    }
    if request.args.get("code") is None:
        d['status'] = 401
        d['message'] = 'Not logged into Spotify' 
    else:
        session['spotify_code'] = request.args["code"]
        session['access_token_obj'] = get_auth_code_obj(session['spotify_code'])
        session['access_token'] = session['access_token_obj']['access_token']
        session['access_token_obj']['expire_date'] = get_expired_date(session['access_token_obj']['expires_in'])
        # d['code'] = session['spotify_code']
    return session['access_token_obj'], d['status']

@auth_app.route('/auth/logout', methods=["GET"])
def spotify_logout():
    session.clear()
    return {'status': 200, 'message': 'Logged out of Spotify successfully'}

@auth_app.route('/playlists', methods=["GET", "PUT"])
@requires_auth
def all_spotify_playlists():
    page_args = request.args.get("page")
    page = 0
    if  page_args is not None: page = (int(page_args)-1) * 10
    url = f'https://api.spotify.com/v1/me/playlists?offset={page}&limit=10'
    header = get_token_header(session['access_token'])
    playlist_response = requests.get(url, headers=header)
    return playlist_response.json()

@auth_app.route('/playlists/<pid>', methods=["GET"])
@requires_auth
def get_spotify_playlist(pid):
    url = f'https://api.spotify.com/v1/playlists/{pid}'
    header = get_token_header(session['access_token'])
    playlist_response = requests.get(url, headers=header)
    return playlist_response.json()

@auth_app.route('/playlists/<pid>/tracks', methods=["GET"])
@requires_auth
def get_spotify_playlist_tracks(pid):
    url = f'https://api.spotify.com/v1/playlists/{pid}/tracks'
    header = get_token_header(session['access_token'])
    playlist_track_response = requests.get(url, headers=header).json()
    return playlist_track_response

@auth_app.route('/tracks/<tid>', methods=["GET"])
@requires_auth
def get_spotify_tracks(tid):
    url = f'https://api.spotify.com/v1/tracks/{tid}'
    header = get_token_header(session['access_token'])
    track_response = requests.get(url, headers=header).json()
    return extract_track(track_response)
    # return track_response

@auth_app.route('/tracks/<tid>/clean', methods=["GET"])
@requires_auth
def search_spotify_clean_tracks(tid):
    url = f'https://api.spotify.com/v1/tracks/{tid}'
    header = get_token_header(session['access_token'])
    track_response = requests.get(url, headers=header).json()
    if not track_response['explicit']:
        return track_response
    current_track_hash = get_track_hash(track_response)

    artist_query = ''
    for artist in track_response['artists']:
        artist_query += f"{artist['name']} "
    search_query = f"{track_response['name']} {artist_query}"
    search_url = f'https://api.spotify.com/v1/search?q={search_query}&type=track'
    search_response = requests.get(search_url, headers=header).json()
    search_response_obj = list()
    for result in search_response['tracks']['items']:
        if not result['explicit']:
            track_hash = get_track_hash(result)
            search_response_obj.append(extract_track(result))
            if track_hash == current_track_hash:
               return extract_track(result)
    
    return search_response_obj

# @auth_app.route('/playlists/<pid>/clean', methods=["GET"])
# @requires_auth
# def clean_spotify_playlist(pid):
#     tracks = list()
#     next = True
#     first = True
#     url = ''
#     while next:
#         if first:
#             url = f'https://api.spotify.com/v1/playlists/{pid}/tracks'
#             first = False
#         header = get_token_header(session['access_token'])
#         playlist_track_response = requests.get(url, headers=header).json()
#         tracks.extend(playlist_track_response['items'])
#         url = playlist_track_response.get('next')
#         print(url)
#         if playlist_track_response['next'] is None:
#             next = False
#             continue
#     return tracks
