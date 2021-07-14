import tweepy
from tweepy import OAuthHandler
import os
import json
from timeit import default_timer as timer


class Twitter:

    def __init__(self, cfg):
        """

        :param cfg: Hydra config for Twitter API
        """
        auth = OAuthHandler((cfg.get('consumer_key', os.environ.get('CONSUMER_KEY'))),
                            (cfg.get('consumer_secret', os.environ.get('CONSUMER_SECRET'))))
        auth.set_access_token((cfg.get('access_token', os.environ.get('ACCESS_TOKEN'))),
                              (cfg.get('access_secret', os.environ.get('ACCESS_SECRET'))))
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def verify_credentials(self) -> None:
        """
        Verify
        """
        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except:
            print("Error during authentication")

    def get_twitter_data(self, df_twt_archive) -> None:
        """
        Query Twitter's API for JSON data for each tweet ID in the Twitter archive

        :param df_twt_archive:
        """
        tweet_ids = df_twt_archive.tweet_id.values

        count = 0
        fails_dict = {}
        start = timer()
        # Save each tweet's returned JSON as a new line in a .txt file
        with open('tweet_json.txt', 'w') as outfile:
            # This loop will likely take 20-30 minutes to run because of Twitter's rate limit
            for tweet_id in tweet_ids:
                count += 1
                print(str(count) + ": " + str(tweet_id))
                try:
                    tweet = self.api.get_status(tweet_id, tweet_mode='extended')
                    print("Success")
                    json.dump(tweet._json, outfile)
                    outfile.write('\n')
                except tweepy.TweepError as e:
                    print("Fail")
                    fails_dict[tweet_id] = e
                    pass
        end = timer()
        print(end - start)
        print(fails_dict)
