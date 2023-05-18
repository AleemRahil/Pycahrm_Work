import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import pandas as pd
import matplotlib.pyplot as plt
import youtube_dl

# YouTube Data API configuration
api_key = "YOUR_API_KEY"
youtube = build('youtube', 'v3', developerKey=api_key)

# Retrieve basic channel information
def get_channel_info(channel_id):
    request = youtube.channels().list(part='snippet,statistics', id=channel_id)
    response = request.execute()
    channel = response['items'][0]
    channel_info = {
        'Name': channel['snippet']['title'],
        'Description': channel['snippet']['description'],
        'Subscribers': int(channel['statistics']['subscriberCount']),
        'Views': int(channel['statistics']['viewCount']),
        'Created': channel['snippet']['publishedAt']
    }
    return channel_info

# Fetch recent videos of a channel
def get_recent_videos(channel_id):
    request = youtube.search().list(part='snippet', channelId=channel_id, order='date', type='video')
    response = request.execute()
    videos = []
    for item in response['items']:
        video = {
            'Title': item['snippet']['title'],
            'Upload Date': item['snippet']['publishedAt'],
            'Duration': '',
            'Views': 0,
            'Likes': 0,
            'Dislikes': 0
        }
        videos.append(video)
    # Fetch video statistics
    video_ids = [item['id']['videoId'] for item in response['items']]
    video_stats = get_video_stats(video_ids)
    for i, video in enumerate(videos):
        if video['Upload Date'] in video_stats:
            stats = video_stats[video['Upload Date']]
            video['Duration'] = stats['duration']
            video['Views'] = stats['views']
            video['Likes'] = stats['likes']
            video['Dislikes'] = stats['dislikes']
    return videos

# Retrieve statistics for a list of videos
def get_video_stats(video_ids):
    request = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids))
    response = request.execute()
    video_stats = {}
    for item in response['items']:
        video_id = item['id']
        stats = {
            'duration': item['contentDetails']['duration'],
            'views': int(item['statistics']['viewCount']),
            'likes': int(item['statistics']['likeCount']),
            'dislikes': int(item['statistics']['dislikeCount'])
        }
        video_stats[video_id] = stats
    return video_stats

# Search for channels based on criteria
def search_channels(query, max_results=10):
    request = youtube.search().list(part='snippet', q=query, type='channel', maxResults=max_results)
    response = request.execute()
    channels = []
    for item in response['items']:
        channel = {
            'Name': item['snippet']['title'],
            'Description': item['snippet']['description'],
            'Subscribers': 0,
            'Views': 0,
            'Created': ''
        }
        channel_id = item['snippet']['channelId']
        channel_info = get_channel_info(channel_id)
        channel.update(channel_info)
        channels.append(channel)
    return channels

# Calculate channel performance statistics
def calculate_channel_stats(channel):
    avg_views = channel['Views'] / channel['Subscribers']
    avg_likes = channel['Likes'] / channel['Subscribers']
    avg_dislikes = channel['Dislikes'] / channel['Subscribers']
    return {
        'Average Views per Video' : avg_views,
        'Average Likes per Video': avg_likes,
        'Average Dislikes per Video': avg_dislikes
    }

# Download video or audio
def download_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example usage
if __name__ == '__main__':
    # Retrieve basic channel information
    channel_id = 'YOUR_CHANNEL_ID'
    channel_info = get_channel_info(channel_id)
    print('Channel Information:')
    for key, value in channel_info.items():
        print(f'{key}: {value}')

    # Fetch recent videos
    videos = get_recent_videos(channel_id)
    print('\nRecent Videos:')
    for video in videos:
        print('---')
        for key, value in video.items():
            print(f'{key}: {value}')

    # Search for channels
    query = 'music'
    channels = search_channels(query)
    print(f'\nChannels related to "{query}":')
    for channel in channels:
        print('---')
        for key, value in channel.items():
            print(f'{key}: {value}')

    # Calculate channel performance statistics
    for channel in channels:
        stats = calculate_channel_stats(channel)
        print('\nChannel Performance Statistics:')
        for key, value in stats.items():
            print(f'{key}: {value}')

    # Download a video
    video_url = 'https://www.youtube.com/watch?v=VIDEO_ID'
    download_video(video_url)
