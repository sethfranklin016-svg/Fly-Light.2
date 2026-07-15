from flask import Flask, render_template, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Jellyfin configuration
JELLYFIN_URL = os.getenv('JELLYFIN_URL', 'http://localhost:8096')
JELLYFIN_API_KEY = os.getenv('JELLYFIN_API_KEY', '')
JELLYFIN_USER_ID = os.getenv('JELLYFIN_USER_ID', '')

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/movies')
def get_movies():
    """Fetch movies from Jellyfin"""
    try:
        headers = {'X-MediaBrowser-Token': JELLYFIN_API_KEY}
        
        # Get all movies
        url = f"{JELLYFIN_URL}/Users/{JELLYFIN_USER_ID}/Items"
        params = {
            'IncludeItemTypes': 'Movie',
            'Recursive': 'true',
            'Fields': 'PrimaryImageAspectRatio,Overview'
        }
        
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        movies = []
        for item in data.get('Items', []):
            movies.append({
                'id': item['Id'],
                'name': item['Name'],
                'overview': item.get('Overview', ''),
                'image': f"{JELLYFIN_URL}/Items/{item['Id']}/Images/Primary"
            })
        
        return jsonify(movies)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/videos')
def get_videos():
    """Fetch videos from Jellyfin"""
    try:
        headers = {'X-MediaBrowser-Token': JELLYFIN_API_KEY}
        
        # Get all videos
        url = f"{JELLYFIN_URL}/Users/{JELLYFIN_USER_ID}/Items"
        params = {
            'IncludeItemTypes': 'Video',
            'Recursive': 'true',
            'Fields': 'PrimaryImageAspectRatio,Overview'
        }
        
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        videos = []
        for item in data.get('Items', []):
            videos.append({
                'id': item['Id'],
                'name': item['Name'],
                'overview': item.get('Overview', ''),
                'image': f"{JELLYFIN_URL}/Items/{item['Id']}/Images/Primary"
            })
        
        return jsonify(videos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/play/<item_id>')
def play_item(item_id):
    """Get playback URL for an item"""
    try:
        url = f"{JELLYFIN_URL}/Videos/{item_id}/stream"
        params = {'static': 'true', 'api_key': JELLYFIN_API_KEY}
        return jsonify({'url': f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)