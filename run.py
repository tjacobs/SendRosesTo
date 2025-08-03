import os
import re
import tweepy
from dotenv import load_dotenv
import sys
import logging
import argparse
sys.path.append('vibe')
from create_poem import create_poem
from create_audio import create_audio
from create_video import create_video

load_dotenv()

# Disable verbose logging (set to WARNING)
logging.basicConfig(level=logging.WARNING)

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
        
        # Debug: log the tweet text being sent
        print("[write] Tweet text to be posted:\n" + text)
        try:
            response = client.create_tweet(text=text, media_ids=media_ids, user_auth=True)
        except tweepy.errors.Forbidden as err:
            print("=== Tweepy Forbidden (403) ===")
            resp = err.response
            print(f"Status code: {resp.status_code}")
            print("Headers:\n", resp.headers)
            try:
                print("Body:\n", resp.json())
            except ValueError:
                print("Body (raw):\n", resp.text)
            raise  # re-raise so the outer handler can also catch it

        print(f"Tweet posted successfully! Tweet ID: {response.data['id']}")
        print(f"Tweet URL: https://twitter.com/user/status/{response.data['id']}")
        return response.data
        
    except Exception as e:
        print(f"Error posting tweet: {e}")
        return None

def read(count=1):
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
            return mentions.data[0].text, mentions.data[0].author_id
        else:
            print("No mentions found.")
            return [], None
            
    except Exception as e:
        print(f"Error reading mentions: {e}")
        return None

def extract_target_tag(tweet_text):
    """Extract @ tags from tweet text, excluding @sendroses2. Returns first external mention."""
    mention_pattern = r'@(?P<tag>\w+)'
    mentions = re.findall(mention_pattern, tweet_text)

    # Debug logging
    print("[extract_target_tag] Raw tweet text:", tweet_text)
    print("[extract_target_tag] Mentions found:", mentions)

    target_tags = [m for m in mentions if m.lower() != 'sendrosesto']
    print("[extract_target_tag] Filtered target_tags (excluding sendrosesto):", target_tags)

    if target_tags:
        chosen = target_tags[0]
        print(f"[extract_target_tag] Returning first target tag: @{chosen}")
        return chosen
    else:
        print("[extract_target_tag] No target tags found (excluding @sendroses2)")
        return None

def get_author_tag(author_id):
    """Get the username/tag from author ID"""
    try:
        client = get_twitter_client()
        user = client.get_user(id=author_id, user_auth=True)
        
        if user.data:
            username = user.data.username
            print(f"Author tag: @{username}")
            return username
        else:
            print("User not found")
            return None
            
    except Exception as e:
        print(f"Error getting author tag: {e}")
        return None

def read_specific_tweet(tweet_url):
    """Read a specific tweet by URL"""
    try:
        # Extract tweet ID from URL
        tweet_id = tweet_url.split('/')[-1].split('?')[0]
        
        client = get_twitter_client()
        
        # Get the specific tweet
        tweet = client.get_tweet(
            id=tweet_id,
            tweet_fields=['created_at', 'author_id', 'public_metrics'],
            user_auth=True
        )
        
        if tweet.data:
            return tweet.data.text, tweet.data.author_id
        else:
            print("Tweet not found.")
            return None, None
            
    except Exception as e:
        print(f"Error reading specific tweet: {e}")
        return None, None

def compose_tweet(author_tag, target_tag, poem):
    """Compose a complete tweet with header, poem, and footer"""
    # Create header
    header = f"@{author_tag} is sending flowers to @{target_tag}"
    
    if not poem:
        poem = "Roses are red, violets are blue,\nThese flowers are sent with love to you."
    
    # Create footer
    footer = "Do you accept? Yes or no.\n\n" #   ; \
#             \
#             "Powered by @inworld_ai, @tenstorrent, @windsurf, @agihouse_org.\n" \
#             "Built by @RyanHolmes100, @TomPJacobs, @kaarelkaarelson.\n\n" \
#             \
#             "(To send your own roses, send a tweet to @sendrosesto and at the person you want to send roses to.)"
    
    # Combine all parts
    tweet_text = f"{header}\n\n{poem}\n\n{footer}"
    
    return tweet_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process tweets and send flower responses')
    parser.add_argument('--tweet-url', help='Process a specific tweet by URL')
    args = parser.parse_args()

    video_path = "video.mp4"
    audio_path = "audio.mp3"
    image_path = "image.jpg"

    # Read tweet based on mode
    if args.tweet_url:
        print(f"Processing specific tweet: {args.tweet_url}")
        tweet_text, author_id = read_specific_tweet(args.tweet_url)
    else:
        print("Reading latest mentions...")
        tweet_text, author_id = read(1)
    
    print(f"Tweet Text: {tweet_text}")
    print(f"Author ID: {author_id}")

    if tweet_text and author_id:
        author_tag = get_author_tag(author_id)
        print(f"Author Tag: {author_tag}")
        
        target_tag = extract_target_tag(tweet_text)
        print(f"Target Tag: {target_tag}")

        print("\nTesting compose_tweet function:")
        if target_tag and author_tag:
            # Generate poem based on target_tag
            prompt = f"make a love poem about how great {target_tag} is"
            poem = create_poem(prompt)
            print(f"Poem:\n{poem}")

            composed_tweet = compose_tweet(author_tag, target_tag, poem)
            print(f"Complete tweet:\n{composed_tweet}")
            
            # Create audio and video    
            audio_path = create_audio(poem, audio_path)
            video_path = create_video(audio_path, image_path, video_path)

            import os
            video_path = os.path.join(os.path.dirname(__file__), "video.mp4")
            print(f"Audio path: {audio_path}")
            print(f"Video path: {video_path}")

            # Post tweet with video
            write(composed_tweet, video_path)
    else:
        print("No valid tweet found to process.")

