from flask import render_template, request, jsonify
import requests
from urllib3.exceptions import NameResolutionError

def index():
    return render_template('index.html')

def search_songs():
    query = request.args.get('q')
    index = request.args.get('index', 0, type=int)
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        response = requests.get(f'https://api.deezer.com/search?q={query}&index={index}', timeout=5)
        response.raise_for_status()
        data = response.json()
        songs = [
            {
                'title': song['title'],
                'artist': song['artist']['name'],
                'album': song['album']['title'],
                'preview': song['preview'],
                'cover_small': song['album'].get('cover_small', '')
            }
            for song in data.get('data', [])
        ]
        next_index = index + len(songs) if len(songs) > 0 else None
        return jsonify({'songs': songs, 'next_index': next_index})
    except NameResolutionError:
        return jsonify({'error': 'Cannot reach Deezer API. Please check your internet connection or DNS settings.'}), 503
    except requests.Timeout:
        return jsonify({'error': 'Request to Deezer API timed out. Please try again later.'}), 504
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to fetch songs: {str(e)}'}), 500