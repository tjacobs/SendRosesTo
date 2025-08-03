import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

def get_twitter_client():
    """Initialize and return Twitter API client"""
    return tweepy.Client(
        consumer_key=os.getenv('TWITTER_API_KEY'),
        consumer_secret=os.getenv('TWITTER_API_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )

def get_twitter_api():
    """Initialize and return Twitter API v1.1 for media uploads"""
    auth = tweepy.OAuthHandler(
        os.getenv('TWITTER_API_KEY'),
        os.getenv('TWITTER_API_SECRET')
    )
    auth.set_access_token(
        os.getenv('TWITTER_ACCESS_TOKEN'),
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
    return tweepy.API(auth)

def write(text, video_path=None):
    """Post a tweet with optional video attachment using v1.1 API"""
    try:
        api = get_twitter_api()
        media_ids = None
        
        if video_path and os.path.exists(video_path):
            print(f"Uploading video: {video_path}")
            media = api.media_upload(video_path)
            media_ids = [media.media_id]
            print(f"Video uploaded! Media ID: {media.media_id}")
        
        response = api.update_status(status=text, media_ids=media_ids)
        
        print(f"Tweet posted successfully! Tweet ID: {response.id}")
        print(f"Tweet URL: https://twitter.com/user/status/{response.id}")
        return response
        
    except Exception as e:
        print(f"Error posting tweet: {e}")
        return None

def read(count=10):
    """Read tweets where the user is mentioned/tagged using v1.1 API"""
    try:
        api = get_twitter_api()
        
        # Get mentions using v1.1 API
        mentions = api.mentions_timeline(count=count, tweet_mode='extended')
        
        if mentions:
            print(f"Found {len(mentions)} mentions:")
            for i, tweet in enumerate(mentions, 1):
                print(f"\n{i}. Tweet ID: {tweet.id}")
                print(f"   Text: {tweet.full_text}")
                print(f"   Created: {tweet.created_at}")
                print(f"   Author: @{tweet.user.screen_name}")
                print(f"   Likes: {tweet.favorite_count}, Retweets: {tweet.retweet_count}")
            
            return mentions
        else:
            print("No mentions found.")
            return []
            
    except Exception as e:
        print(f"Error reading mentions: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    print("Testing write function:")
    #write("Testing the new write function! 🚀", "/ai_commerce/amazon_ai_agent/video.mp4")
    
    print("\nTesting read function:")
    read(1)