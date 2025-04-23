# import os
# from flask import Flask, render_template, send_file, jsonify, request
# from audioScanner import AudioScanner
#
# app = Flask(__name__)
#
# # Initialize scanner with root directory (user’s home directory by default)
# scanner = AudioScanner("~/Music")  # Update to desired path, e.g., "~" or "/path/to/music"
#
# @app.route('/')
# def index():
#     """Render the main page with a list of audio files."""
#     return render_template('index.html', audio_files=scanner.get_audio_files())
#
# @app.route('/scan', methods=['POST'])
# def scan_audio():
#     """Trigger a filesystem scan and return the result."""
#     audio_files = scanner.scan()
#     return jsonify({'status': 'success', 'count': len(audio_files)})
#
# @app.route('/play/<path:filename>')
# def play_audio(filename):
#     """Serve an audio file for playback."""
#     if os.path.exists(filename) and os.path.splitext(filename)[1].lower() in AudioScanner.AUDIO_EXTENSIONS:
#         return send_file(filename)
#     return "File not found", 404
#
# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, send_file, jsonify, request
from audio_scanner import AudioScanner
import os

app = Flask(__name__)

# Use /tmp for scanning in Vercel’s serverless environment (read-only filesystem except /tmp)
SCAN_ROOT = os.environ.get('SCAN_ROOT', '/tmp')
scanner = AudioScanner(SCAN_ROOT)

@app.route('/')
def index():
    """Render the main page with a list of audio files."""
    return render_template('index.html', audio_files=scanner.get_audio_files())

@app.route('/scan', methods=['POST'])
def scan_audio():
    """Trigger a filesystem scan and return the result."""
    audio_files = scanner.scan()
    return jsonify({'status': 'success', 'count': len(audio_files)})

@app.route('/play/<path:filename>')
def play_audio(filename):
    """Serve an audio file for playback."""
    if os.path.exists(filename) and os.path.splitext(filename)[1].lower() in AudioScanner.AUDIO_EXTENSIONS:
        return send_file(filename)
    return "File not found", 404

if __name__ == '__main__':
    # Run in debug mode locally, but not on Vercel
    app.run(debug=not os.environ.get('VERCEL', False))