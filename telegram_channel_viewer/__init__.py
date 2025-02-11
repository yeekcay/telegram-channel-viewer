import requests
from bs4 import BeautifulSoup

class Post:
    def __init__(self, channel, post_id):
        self.channel = channel
        self.post_id = post_id
        self._fetch_post_data()

    def _fetch_post_data(self):
        url = f'https://t.me/{self.channel}/{self.post_id}?embed=1&mode=tme'
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, 'html.parser')

    @property
    def content(self):
        message_div = self.soup.find('div', class_='tgme_widget_message_text')
        return message_div.text if message_div else None

    @property
    def date(self):
        time_elem = self.soup.find('time', class_='datetime')
        return time_elem.text if time_elem else None

    @property
    def views(self):
        views_span = self.soup.find('span', class_='tgme_widget_message_views')
        return views_span.text if views_span else None

class LatestMessage:
    def __init__(self, channel_name):
        self.channel = channel_name.replace("@", "")
        self._fetch_latest_data()

    def _fetch_latest_data(self):
        url = f'https://t.me/s/{self.channel}/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get the last message link
        message_dates = soup.find_all('a', class_='tgme_widget_message_date')
        if message_dates:
            latest_link = message_dates[-1]['href']
            self.message_id = latest_link.split('/')[-1]
            
            # Fetch detailed message data
            post_url = f'https://t.me/{self.channel}/{self.message_id}?embed=1&mode=tme'
            post_response = requests.get(post_url)
            self.post_soup = BeautifulSoup(post_response.text, 'html.parser')

    @property
    def content(self):
        message_div = self.post_soup.find('div', class_='tgme_widget_message_text')
        return message_div.text if message_div else None

    @property
    def date(self):
        time_elem = self.post_soup.find('time', class_='datetime')
        return time_elem.text if time_elem else None

    @property
    def views(self):
        views_span = self.post_soup.find('span', class_='tgme_widget_message_views')
        return views_span.text if views_span else None

    def __str__(self):
        return self.message_id

class TGView:
    def __init__(self, channel):
        self.channel = channel.replace("@", "") if channel.startswith("@") else channel
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self._fetch_data()

    def _fetch_data(self):
        url = f'https://t.me/{self.channel}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, 'html.parser')

    @property
    def channel_name(self):
        meta = self.soup.find('meta', property='og:title')
        return meta['content'] if meta else None

    @property
    def channel_profile(self):
        meta = self.soup.find('meta', property='og:image')
        return meta['content'] if meta else None

    @property
    def channel_description(self):
        meta = self.soup.find('meta', property='og:description')
        return meta['content'] if meta else None

    @property
    def channel_subs(self):
        subscribers_div = self.soup.find('div', class_='tgme_page_extra')
        return subscribers_div.text.strip() if subscribers_div else None

    @property
    def channel_latest_message(self):
        return LatestMessage(self.channel)

    def post(self, post_id):
        return Post(self.channel, post_id)

def channel(channel_username):
    return TGView(channel_username)
