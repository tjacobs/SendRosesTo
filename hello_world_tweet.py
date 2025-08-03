import os
import re
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
    """Post a tweet with optional video attachment using v2 API"""
    try:
        client = get_twitter_client()
        media_ids = None
        
        if video_path and os.path.exists(video_path):
            print(f"Uploading video: {video_path}")
            api = get_twitter_api()
            media = api.media_upload(video_path)
            media_ids = [media.media_id]
            print(f"Video uploaded! Media ID: {media.media_id}")
        
        response = client.create_tweet(text=text, media_ids=media_ids, user_auth=True)
        
        print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
        print(f"Tweet URL: https://twitter.com/user/status/{response.data['id']}")
        return response.data
        
    except Exception as e:
        print(f"Error posting tweet: {e}")
        return None

def read(count=10):
    """Read tweets where the user is mentioned/tagged using v2 API"""
    try:
        client = get_twitter_client()
        
        # Get the authenticated user's ID
        me = client.get_me(user_auth=True)
        user_id = me.data.id
        
        # Get mentions using v2 API (max_results must be 5-100)
        max_results = max(5, min(100, count))
        mentions = client.get_users_mentions(
            id=user_id,
            max_results=max_results,
            tweet_fields=['created_at', 'author_id', 'public_metrics'],
            user_auth=True
        )
        
        if mentions.data:
            print(f"Found {len(mentions.data)} mentions:")
            for i, tweet in enumerate(mentions.data, 1):
                print(f"\n{i}. Tweet ID: {tweet.id}")
                print(f"   Text: {tweet.text}")
                print(f"   Created: {tweet.created_at}")
                print(f"   Author ID: {tweet.author_id}")
                if tweet.public_metrics:
                    print(f"   Likes: {tweet.public_metrics['like_count']}, Retweets: {tweet.public_metrics['retweet_count']}")
            
            return mentions.data
        else:
            print("No mentions found.")
            return []
            
    except Exception as e:
        print(f"Error reading mentions: {e}")
        return None

def extract_target_tag(tweet_text):
    """Extract @ tags from tweet text, excluding @sendroses2"""
    mention_pattern = r'@(\w+)'
    mentions = re.findall(mention_pattern, tweet_text) #"Hello @sendroses2, sending roses to @test") #tweet_text "")
    
    target_tags = [mention for mention in mentions if mention.lower() != 'sendroses2']
    
    if target_tags:
        return target_tags[0]
    else:
        print("No target tags found (excluding @sendroses2)")
        return []

if __name__ == "__main__":
    # Read text from poem.txt
    poem_path = "poem.txt"
    video_path = "video.mp4"
    
    try:
        with open(poem_path, 'r', encoding='utf-8') as f:
            poem_text = f.read().strip()
        
        print("Testing write function:")
        print(f"Poem text: {poem_text}")
        #write(poem_text, video_path)
        
    except FileNotFoundError:
        print(f"Error: {poem_path} not found. Please run the vibe/main.py first to generate the poem.")
        print("Falling back to default text...")
        #write("Testing the new write function! 🚀", video_path)
    
    print("\nTesting read function:")
    #read(1)

    print("\nTesting extract_target_tag function:")
    target_tag = extract_target_tag("Hello @sendroses2, sending roses to @test")
    print(f"Target Tag: {target_tag}")

