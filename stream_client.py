import json

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_config

        
class Listener(tweepy.Stream):
    
    def get_tw_dict(self, tweet):
        if "extended_tweet" in tweet:
            text = tweet["extended_tweet"]["full_text"]
        else:
            text = tweet['text']
            
        tw = {"id": tweet['id_str'],
              "created_at": tweet['created_at'],
              "text": tweet["text"],
              "username": tweet["user"]["screen_name"],
              "followers": tweet["user"]["followers_count"],
              "retweets": tweet['retweet_count'],
              "favorites": tweet['favorite_count']}
        return tw
    
    
    def on_data(self, data):
        tweet = json.loads(data)
        if tweet['retweeted'] == False and 'RT' not in tweet['text'] and tweet['in_reply_to_status_id'] == None:
            tw = self.get_tw_dict(tweet)
            # post this print(json.dumps(tw))
    
    
    def on_error(self, status):
        print(status)
        
if __name__ == "__main__":
    hash_tag_list = ["SHIBARMY", "SHIB"]
    stream = Listener(twitter_config.CONSUMER_KEY, twitter_config.CONSUMER_SECRET,
                         twitter_config.ACCESS_TOKEN, twitter_config.ACCESS_TOKEN_SECRET)
    stream.filter(track=hash_tag_list)
    

    