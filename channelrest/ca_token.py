import os
import requests
import json
import datetime
from requests.auth import HTTPBasicAuth
import os.path
from os import path

class ChannelAdvisorToken:
    def __init__(self, client_id, client_secret, refresh_token_ca, refresh_url = "https://api.channeladvisor.com/oauth2/token"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token_ca = refresh_token_ca
        self.refresh_url = refresh_url
        self.cache_file = refresh_token_ca + ".json"

    def refresh_token(self):
        basic = HTTPBasicAuth(self.client_id, self.client_secret)

        headers = {
            'User-Agent': 'My User Agent 1.0',
            'Content-Type': "application/x-www-form-urlencoded",
        }

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token_ca
        }
        
        # print(data)

        r = requests.post(self.refresh_url, auth=basic, headers=headers, data=data)
        token_data = r.json()

        # print(token_data)
        expiration_time =  datetime.datetime.now(datetime.timezone.utc) +  datetime.timedelta(seconds=token_data['expires_in'])
        token_data['expiration_date'] =   int(expiration_time.timestamp())

        with open(self.cache_file, "w") as outfile:
            json.dump(token_data, outfile)
        return token_data

    def get_token(self):
        #Reading cache
        if path.exists(self.cache_file):
            with open(self.cache_file, "r") as infile:
                token_data = json.load(infile)
            # print(int(datetime.datetime.now(datetime.timezone.utc).timestamp()))
            # print(token_data['expiration_date'])
            if int(datetime.datetime.now(datetime.timezone.utc).timestamp()) > token_data['expiration_date']:
                #Token expired, get new
                token_data = self.refresh_token()
        else:
            #No cached value, get and cache
            token_data = self.refresh_token()

        return token_data['access_token']