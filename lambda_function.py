import requests
from requests_oauthlib import OAuth1Session
import time
from datetime import datetime, date
import math
import yaml
from pytz import timezone



def build_url(name):
    '''
    given the name for profile (not username), the function builds the url to post to which will update the bio accordingly
    '''
    # calculate how long since last michigan championship
    last_michigan_championship = datetime(2004, 11, 20, 16, 43)
    print(str(last_michigan_championship.year))
    now = datetime.now()
    difference = datetime.now() - last_michigan_championship
    years = math.floor(difference.days / 365.25)
    days = math.floor(difference.days - (years * 365.25))
    hours = difference.seconds // 3600
    minutes = (difference.seconds // 60) % 60

    # add the time to the beginning of the bio
    tz = timezone('America/Detroit')
    t = datetime.now(tz)
    pmam = 'PM'
    if t.hour < 12:
        pmam = 'AM'
    hour = t.hour % 12
    minute = t.minute

    bio = f"It is {hour}:{minute} {pmam} on {date.today().strftime('%B %d, %Y')} and it has been {years} years, {days} days, {hours} hours, and {minutes} minutes since Michigan football last won a B1G championship."
    
    # remove plurals if time increments are 1
    if years == 1:
        bio = bio.replace('years', 'year')
    if days == 1:
        bio = bio.replace('days', 'day')
    if hours == 1:
        bio = bio.replace('hours', 'hour')
    if minutes == 1:
        bio = bio.replace('minutes', 'minute')

    # combine the bio with proper endpoint
    url = 'https://api.twitter.com/1.1/account/update_profile.json?name=' + name + '&description=' + bio
    # how you indicate spaces in url
    url = url.replace(' ', '%20') # html encoding for space is %20
    url = url.replace(':', '%3A').replace('%3A', ':', 1) # html encoding for : is %3A, but we don't want the first colon replaced in https://

    return url

def lambda_handler(even, context):
    # read in api keys from yaml file (not included in this repository for security reasons)
    with open('keys.yaml', 'r') as stream:
        keys = yaml.load(stream)
    consumer_key = keys['api_key']
    consumer_secret = keys['api_secret_key']
    access_token = keys['access_token']
    access_token_secret = keys['access_token_secret']

    # open connection to twitter API
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    response = oauth.post(build_url("AJ Bensman"))
