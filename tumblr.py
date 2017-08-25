#!/usr/bin/env python
import requests
from requests_oauthlib import OAuth1
import configparser, os

config = configparser.ConfigParser()
config.read_file(open('.settings.ini'))

AUTH_URL = "https://www.tumblr.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.tumblr.com/oauth/access_token"
REQUEST_TOKEN_URL = "https://www.tumblr.com/oauth/request_token"
API_URL = "https://api.tumblr.com"
BLOGS = 'blogs'
OFFSET_COUNT = 20

CONSUMER_KEY = config.get('DEFAULT', 'CONSUMER_KEY')
CONSUMER_SECRET = config.get('DEFAULT', 'CONSUMER_SECRET')
TOKEN = config.get('DEFAULT', 'TOKEN')
TOKEN_SECRET = config.get('DEFAULT', 'TOKEN_SECRET')
API_KEY = config.get('DEFAULT', 'API_KEY')

FOLLOWING = 'https://api.tumblr.com/v2/user/following'
UNFOLLOW = 'https://api.tumblr.com/v2/user/unfollow'


oauth = OAuth1(
  CONSUMER_KEY, 
  client_secret=CONSUMER_SECRET,
  resource_owner_key=TOKEN,
  resource_owner_secret=TOKEN_SECRET
  )


# Get data from tumblr
def get_remote_data(url, my_auth, my_params):
  r = requests.get(url, auth=my_auth, params=my_params)
  data = r.json()
  return data


# Post data from tumbl
def post_remote_data(url, my_auth, url_params):
  return requests.post(url, auth=my_auth, data=url_params)

# Unfollow blogs
def process_unfollow(blogs):
  for blog in blogs:
    url = blog.get('url')
    param = {'url': url}
    result = post_remote_data(UNFOLLOW, oauth, param) 
    print(url, result)


# Get the list of data
def process_list(blogs):
  for blog in blogs:
    data = {
      'url': blog.get('url'),
      'name': blog.get('name'),
      'title': blog.get('title'),
      'description': blog.get('description')
    }
    print(data['url'])


# Retrieve data from tumblr
def get_data(action=FOLLOWING, offset=0, limit=20):
  params = {"offset": offset, "limit": limit}
  response = get_remote_data(action, oauth, params)
  status = response.get('meta').get('status')
  if status > 400:
    message = response.get('meta').get('msg')
    try:
      raise RuntimeError(message)
    finally:
      print("Response:", response.get('meta').get('status'))
      print("Error:", message)
    
  data = response.get('response')
  return data


# Get list of blogs being followed
def get_all_data():
  has_more = True
  page_count = 0
  offset = 0
  while True:
    yield get_data(offset=offset)
    page_count = page_count + 1
    offset = (page_count * OFFSET_COUNT)


# Retrieve current page
def get_current_page():
  while True:
    yield get_data(offset=0)


# Unfollow blogs
def unfollow_blogs():
  for value in get_current_page():
    blogs = value[BLOGS]
    process_unfollow(blogs)
    if(len(blogs) < OFFSET_COUNT):
      break


# Process individual blogs
def blog_action(action):
  for value in get_all_data():
    blogs = value[BLOGS]
    action(blogs)
    if (len(blogs) < OFFSET_COUNT):
      break


def main():
  blog_action(process_list)
  unfollow_blogs()
  
main()
