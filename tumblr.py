#!/usr/bin/env python
import requests
from requests_oauthlib import OAuth1
from urllib.parse import parse_qs
from math import ceil

AUTH_URL = "https://www.tumblr.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.tumblr.com/oauth/access_token"
REQUEST_TOKEN_URL = "https://www.tumblr.com/oauth/request_token"
API_URL = "https://api.tumblr.com"

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
TOKEN = ""
TOKEN_SECRET = ""
API_KEY = ""

FOLLOWING = 'https://api.tumblr.com/v2/user/following'
UNFOLLOW = 'https://api.tumblr.com/v2/user/unfollow'

oauth = OAuth1(
  CONSUMER_KEY, 
  client_secret=CONSUMER_SECRET,
  resource_owner_key=TOKEN,
  resource_owner_secret=TOKEN_SECRET,
  signature_type='auth_header')

def get_data(url, my_auth, my_params):
  r = requests.get(url, auth=my_auth, params=my_params)
  data = r.json()
  return data

def unfollow(url, my_auth, url_params):
  return requests.post(url, auth=my_auth, data=url_params)

def process_current_blogs(blogs):
  for blog in blogs:
    url = blog.get('url')
    param = {'url': url}
    result = unfollow(UNFOLLOW, oauth, param) 
    print(url, result)

def process_blogs():
  params = {"offset": 0, "limit": 20}
  data = get_data(FOLLOWING, oauth, params)
  blogs = data.get('response')
  current_blogs = blogs['blogs']
  total_blogs = blogs['total_blogs']
  total_pages = ceil(total_blogs / 20)
  process_current_blogs(current_blogs)
  print(current_blogs)
  
  for x in range (1, total_pages):
    offset = (x * 20) + 1
    print("offset", offset)
    params = {'offset': offset, 'limit': 20}
    data = get_data(FOLLOWING, oauth, params)
    blogs = data.get('response')
    current_blogs = blogs['blogs']
    process_current_blogs(current_blogs)

current_blogs = process_blogs()

# process_current_blogs(current_blogs)
