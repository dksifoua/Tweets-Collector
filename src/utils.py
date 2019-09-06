from datetime import datetime


def extract_features(raw_data):
    tweet = {}

    try:
        tweet['created_at'] = datetime.strptime(raw_data['created_at'], '%a %b %d %H:%M:%S %z %Y')
        tweet['id'] = raw_data['id']
        tweet['user_name'] = raw_data['user']['name']
        tweet['user_screen_name'] = raw_data['user']['screen_name']
        tweet['user_favourites_count'] = raw_data['user']['favourites_count']
        tweet['user_followers_count'] = raw_data['user']['followers_count']
        tweet['user_friends_count'] = raw_data['user']['friends_count']
        tweet['user_statuses_count'] = raw_data['user']['statuses_count']
    except KeyError:
        return None

    # Get the original tweet
    try:
        raw_data = raw_data['retweeted_status']
    except KeyError:
        pass
    tweet['favorite_count'] = raw_data['favorite_count']
    tweet['quote_count'] = raw_data['quote_count']
    tweet['reply_count'] = raw_data['reply_count']
    tweet['retweet_count'] = raw_data['retweet_count']
    tweet['favorite_count'] = raw_data['favorite_count']
    tweet['text'] = raw_data['extended_tweet']['full_text'] if raw_data['truncated'] else raw_data['text']

    return tweet
