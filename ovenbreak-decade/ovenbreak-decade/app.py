from flask import Flask, render_template, request, jsonify, session
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session handling

# Anniversary date: October 27, 2016 (launch) and October 27, 2026 (10th anniversary)
ANNIVERSARY_DATE = datetime(2026, 10, 27, 0, 0, 0)

def get_countdown():
    now = datetime.now()
    if now < ANNIVERSARY_DATE:
        diff = ANNIVERSARY_DATE - now
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return {
            'type': 'countdown',
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }
    elif now == ANNIVERSARY_DATE.replace(hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond):
        # This is unlikely to hit exactly, so we'll check for the day
        return {
            'type': 'anniversary',
            'message': 'Happy 10th Anniversary!'
        }
    else:
        return {
            'type': 'celebration',
            'message': 'Celebrating 10 Years of CookieRun: OvenBreak!'
        }

@app.route('/')
def index():
    countdown_info = get_countdown()
    return render_template('index.html', countdown=countdown_info)

# For the mini-game, we'll serve the game via the same template but we can have a separate route if needed.
# However, the requirement is to have a single page application. We'll use AJAX for the Memory Oven and the game will be on the same page.

# Memory Oven endpoints
@app.route('/api/memory', methods=['POST'])
def add_memory():
    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    favorite_cookie = data.get('favorite_cookie', '').strip()

    if not content:
        return jsonify({'error': 'Memory content is required'}), 400

    # In a real app, we would save to a database, but for this project we use localStorage via the frontend.
    # So we just return the data to be stored by the frontend.
    return jsonify({
        'id': datetime.now().timestamp(),  # Simple ID
        'title': title,
        'content': content,
        'favorite_cookie': favorite_cookie,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/memory/<memory_id>', methods=['PUT'])
def update_memory(memory_id):
    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    favorite_cookie = data.get('favorite_cookie', '').strip()

    if not content:
        return jsonify({'error': 'Memory content is required'}), 400

    return jsonify({
        'id': memory_id,
        'title': title,
        'content': content,
        'favorite_cookie': favorite_cookie,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/memory/<memory_id>', methods=['DELETE'])
def delete_memory(memory_id):
    # In a real app, we would delete from the database.
    # For now, we just return success.
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)