import requests
import os
import base64

def get_auth_code_obj(spotify_code=None, refresh_token=None):
    body = {}
    body['code'] = refresh_token
    body['grant_type'] = 'refresh_token'
    if refresh_token is None:
        body['code'] = spotify_code
        body['grant_type'] = 'authorization_code'
    url = 'https://accounts.spotify.com/api/token'
    redirect_url = os.getenv('APP_BASE_URL')+'/spotify/auth/callback/'
    body['redirect_uri'] = redirect_url
    auth_code_req = requests.post(url, headers=get_header(), data=body)
    return auth_code_req.json()

def get_header():
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    spotify_app_base64 = base64_string(f'{CLIENT_ID}:{CLIENT_SECRET}')
    return {
        'Authorization': f'Basic {spotify_app_base64}'
    }

def get_token_header(access_token):
    return {
        'Authorization': f'Bearer {access_token}'
    }

def base64_string(string):
    encoded_string = base64.b64encode(string.encode('utf-8'))
    return encoded_string.decode('utf-8')