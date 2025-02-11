# telegram-channel-viewer
a python library that can view telegram channels without making a telegram app!

## How It Works

The telegram-channel-viewer module operates by intelligently parsing public Telegram web pages:

1. Channel Information:
   - Fetches data from `https://t.me/{channel_name}`
   - Extracts metadata from OpenGraph tags for accurate channel details
   - Parses subscriber count from the page HTML

2. Latest Messages:
   - Accesses `https://t.me/s/{channel_name}`
   - Identifies the most recent message using message date selectors
   - Extracts message content, date, and view count

3. Specific Posts:
   - Retrieves post data from `https://t.me/{channel_name}/{post_id}?embed=1&mode=tme`
   - Parses the embedded message format for consistent data extraction
   - Provides clean, formatted content without HTML markup

The module uses requests for fetching data and BeautifulSoup4 for efficient HTML parsing, ensuring reliable performance without requiring Telegram API credentials.

# Examples

## Basic Channel Information
```python
from telegram_channel_viewer import channel

# Initialize channel viewer
ch = channel("@durov")

# Get basic channel info
print(f"Channel Name: {ch.channel_name}")
print(f"Description: {ch.channel_description}")
print(f"Subscribers: {ch.channel_subs}")
print(f"Profile Picture: {ch.channel_profile}")

```

## Get the latest message details
```python
latest = ch.channel_latest_message

print("Latest Message Details:")
print(f"Content: {latest.content}")
print(f"Posted on: {latest.date}")
print(f"Views: {latest.views}")
print(f"Message ID: {latest}")
```

## Get a specific post by ID
```python
post = ch.post("1234")

print("Specific Post Details:")
print(f"Content: {post.content}")
print(f"Posted on: {post.date}")
print(f"Views: {post.views}")
```
## This Project is Developed by Claude 3.5
