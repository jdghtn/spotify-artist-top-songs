import os, base64, json

from dotenv import load_dotenv
from requests import post, get

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
  auth_string = client_id + ':' + client_secret
  auth_bytes = auth_string.encode('utf-8')
  auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
  url = 'https://accounts.spotify.com/api/token'

  headers = {
    'Authorization': 'Basic ' + auth_base64,
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  data = {
    'grant_type': 'client_credentials'
  }

  result = post(url, headers = headers, data = data)
  json_result = json.loads(result.content)
  token = json_result['access_token']
   
  return token

def get_auth_header(token):
  return {'Authorization': 'Bearer ' + token}

def artist_search(token, artist):
  url = 'https://api.spotify.com/v1/search'
  headers = get_auth_header(token)
  query = f'?q={artist}&type=artist&limit=1'
  query_url = url + query
  result = get(query_url, headers = headers)
  json_result = json.loads(result.content)['artists']['items']
  
  return json_result[0]

def get_songs_by_artist(token, artist_id):
  url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'

  headers = get_auth_header(token)
  result = get(url, headers = headers)
  json_result = json.loads(result.content)['tracks']

  return json_result

artist = input('Enter your favourite artist: ').title()
token = get_token()
result = artist_search(token, artist)
artist_id = result['id']
songs = get_songs_by_artist(token, artist_id)

print(f'{artist}\'s top 10 songs: ')

for count, song in enumerate(songs):
  print(f'{count + 1}. {song["name"]}')
