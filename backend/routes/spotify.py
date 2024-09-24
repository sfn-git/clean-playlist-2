from flask import Blueprint, redirect, request, session
from urllib.parse import urlencode
from utils.spotify import get_auth_code_obj, get_token_header
import os
import requests

auth_app = Blueprint('auth', __name__)

@auth_app.route('/auth', methods=["GET", "POST"])
def spotify_auth():
    if session.get('spotify_code') is None:
        redirect_url = os.getenv('APP_BASE_URL')+'/spotify/auth/callback/'
        query_parameters = {
            'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
            'response_type': 'code',
            'redirect_uri': redirect_url,
            'scope': 'playlist-modify-public',
        }
        spotify_url = 'https://accounts.spotify.com/authorize?' + urlencode(query_parameters)
        return {'status':200, 'message': spotify_url}
    else:
        d = {'status': 100, 'message': 'Already authenticated'}
        return d, 100

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
        # d['code'] = session['spotify_code']
    return session['access_token_obj'], d['status']

@auth_app.route('/auth/logout', methods=["GET"])
def spotify_logout():
    session.clear()
    return {'status': 200, 'message': 'Logged out of Spotify successfully'}

@auth_app.route('/playlists', methods=["GET", "PUT"])
def spotify_playlists():
    if session.get('access_token') is None:
        d = {'status': 401, 'message': 'Not authorized to view resource'}
        return d, 401
    else:
        url = 'https://api.spotify.com/v1/me/playlists'
        header = get_token_header(session['access_token'])
        playlist_response = requests.get(url, headers=header)
        return playlist_response.json()


