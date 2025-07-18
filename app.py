# Facebook Unfriend Tracker - Compact Web App
import json
import csv
import os
import sqlite3
import secrets
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, flash, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)
# Use environment variable or generate secure secret key
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_urlsafe(32))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
CSV_FOLDER = 'data'
DATABASE = 'friends_tracker.db'
ALLOWED_EXTENSIONS = {'json'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CSV_FOLDER, exist_ok=True)

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create friends table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active',
            facebook_timestamp INTEGER DEFAULT 0
        )
    ''')
    
    # Create unfriends table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unfriends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unfriended_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_seen DATETIME
        )
    ''')
    
    # Create tracking_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracking_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_friends INTEGER,
            unfriended_count INTEGER,
            new_friends_count INTEGER,
            check_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_friends_from_json(file_path):
    """Extract friends list from Facebook JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Handle different possible structures
        friends = []
        if 'friends' in data:
            friends = data['friends']
        elif 'friends_v2' in data:
            friends = data['friends_v2']
        elif isinstance(data, list):
            friends = data
            
        # Extract names and timestamps
        friend_data = []
        for friend in friends:
            if isinstance(friend, dict):
                name = friend.get('name', '')
                timestamp = friend.get('timestamp', 0)
                
                if not name:
                    # Try other possible keys
                    name = friend.get('display_name', '') or friend.get('full_name', '')
                
                if name:
                    # Convert timestamp to readable date
                    if timestamp:
                        try:
                            friend_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                        except:
                            friend_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        friend_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    friend_data.append({
                        'name': name,
                        'timestamp': timestamp,
                        'date_added': friend_date
                    })
            elif isinstance(friend, str):
                friend_data.append({
                    'name': friend,
                    'timestamp': 0,
                    'date_added': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
        return friend_data
    except Exception as e:
        print(f"Error extracting friends: {e}")
        return []

def save_friends_to_csv(friends_data, filename=None):
    """Save friends data to CSV file"""
    if filename is None:
        filename = f"friends_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    filepath = os.path.join(CSV_FOLDER, filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Facebook_Date_Added', 'Timestamp', 'Status', 'Tracked_Date'])
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for friend in friends_data:
            writer.writerow([
                friend['name'], 
                friend['date_added'], 
                friend['timestamp'], 
                'active',
                current_time
            ])
    
    return filepath

def save_unfriends_to_csv(unfriends_list, filename=None):
    """Save unfriended users to CSV file"""
    if filename is None:
        filename = f"unfriends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    filepath = os.path.join(CSV_FOLDER, filename)
    
    # Check if file exists to determine if we need headers
    file_exists = os.path.exists(filepath)
    
    with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        if not file_exists:
            writer.writerow(['Name', 'Unfriended_Date', 'Unfriended_Time'])
        
        current_datetime = datetime.now()
        for friend in unfriends_list:
            writer.writerow([
                friend, 
                current_datetime.strftime('%Y-%m-%d'),
                current_datetime.strftime('%H:%M:%S')
            ])
    
    return filepath

def update_database_with_friends(friends_data):
    """Update database with current friends data"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get current friends from database
    cursor.execute("SELECT name FROM friends WHERE status = 'active'")
    current_friends = set(row[0] for row in cursor.fetchall())
    
    new_friends = set(friend['name'] for friend in friends_data)
    
    # Find unfriended users
    unfriended = current_friends - new_friends
    
    # Find new friends
    newly_added = new_friends - current_friends
    
    # Mark unfriended users as inactive
    for friend in unfriended:
        cursor.execute("""
            UPDATE friends SET status = 'inactive' WHERE name = ? AND status = 'active'
        """, (friend,))
        
        # Add to unfriends table
        cursor.execute("""
            INSERT INTO unfriends (name, unfriended_date) VALUES (?, ?)
        """, (friend, datetime.now()))
    
    # Add new friends with their original Facebook timestamp
    for friend in friends_data:
        if friend['name'] in newly_added:
            cursor.execute("""
                INSERT INTO friends (name, timestamp, status, facebook_timestamp) 
                VALUES (?, ?, 'active', ?)
            """, (friend['name'], datetime.now(), friend['timestamp']))
    
    # Update tracking history
    cursor.execute("""
        INSERT INTO tracking_history (total_friends, unfriended_count, new_friends_count)
        VALUES (?, ?, ?)
    """, (len(new_friends), len(unfriended), len(newly_added)))
    
    conn.commit()
    conn.close()
    
    return list(unfriended), list(newly_added)

def get_unfriends_from_db(days=30):
    """Get unfriends from database within specified days"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    cursor.execute("""
        SELECT name, unfriended_date FROM unfriends 
        WHERE unfriended_date >= ?
        ORDER BY unfriended_date DESC
    """, (cutoff_date,))
    
    unfriends = cursor.fetchall()
    conn.close()
    
    return unfriends

def scheduled_check():
    """Scheduled function to check for unfriends (if there's stored data)"""
    # This would be called by the scheduler
    # For now, it's a placeholder - in a real scenario, you'd need to
    # implement automatic data fetching or manual uploads
    pass

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/spreadsheet')
def spreadsheet():
    """Spreadsheet view page"""
    return render_template('spreadsheet.html')

@app.route('/schedule')
def schedule():
    """Schedule management page"""
    return render_template('schedule.html')

@app.route('/api/friends')
def api_friends():
    """API endpoint for friends data"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name, status, timestamp, facebook_timestamp 
        FROM friends 
        ORDER BY timestamp DESC
    """)
    
    friends = []
    for row in cursor.fetchall():
        name, status, timestamp, facebook_timestamp = row
        
        # Format dates
        tracked_date = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d') if timestamp else 'N/A'
        
        if facebook_timestamp:
            try:
                facebook_date = datetime.fromtimestamp(facebook_timestamp).strftime('%Y-%m-%d')
            except:
                facebook_date = 'N/A'
        else:
            facebook_date = 'N/A'
            
        friends.append({
            'name': name,
            'status': status,
            'facebook_date': facebook_date,
            'tracked_date': tracked_date,
            'last_update': tracked_date
        })
    
    conn.close()
    return jsonify(friends)

@app.route('/api/schedule', methods=['GET', 'POST'])
def api_schedule():
    """API endpoint for schedule management"""
    if request.method == 'POST':
        data = request.json
        # Here you would implement schedule management
        # For now, return success
        return jsonify({'status': 'success', 'message': 'Schedule updated'})
    else:
        # Return current schedule status
        return jsonify({
            'status': 'active',
            'interval': 'daily',
            'next_check': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Extract friends
        friends_data = extract_friends_from_json(filepath)
        
        if not friends_data:
            flash('Could not extract friends from the file. Please check the file format.')
            return redirect(url_for('index'))
        
        # Save to CSV
        csv_filepath = save_friends_to_csv(friends_data)
        
        # Update database and get unfriends
        unfriended, newly_added = update_database_with_friends(friends_data)
        
        # Save unfriends to CSV if any
        if unfriended:
            save_unfriends_to_csv(unfriended)
        
        flash(f'Successfully processed {len(friends_data)} friends. Found {len(unfriended)} unfriends and {len(newly_added)} new friends.')
        
        return render_template('results.html', 
                             total_friends=len(friends_data),
                             unfriended=unfriended,
                             newly_added=newly_added,
                             csv_path=csv_filepath)
    
    flash('Invalid file type. Please upload a JSON file.')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Dashboard showing recent activity"""
    # Get recent unfriends
    recent_unfriends = get_unfriends_from_db(30)
    
    # Get tracking history
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT total_friends, unfriended_count, new_friends_count, check_date 
        FROM tracking_history 
        ORDER BY check_date DESC LIMIT 10
    """)
    
    history = cursor.fetchall()
    
    # Get current stats
    cursor.execute("SELECT COUNT(*) FROM friends WHERE status = 'active'")
    current_friends = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM unfriends")
    total_unfriends = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('dashboard.html',
                         recent_unfriends=recent_unfriends,
                         history=history,
                         current_friends=current_friends,
                         total_unfriends=total_unfriends)

@app.route('/download_csv/<csv_type>')
def download_csv(csv_type):
    """Download CSV files"""
    if csv_type == 'friends':
        # Generate current friends CSV
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, timestamp, status FROM friends ORDER BY timestamp DESC")
        friends = cursor.fetchall()
        conn.close()
        
        filename = f"current_friends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(CSV_FOLDER, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Date_Added', 'Status'])
            writer.writerows(friends)
            
    elif csv_type == 'unfriends':
        # Generate unfriends CSV
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, unfriended_date FROM unfriends ORDER BY unfriended_date DESC")
        unfriends = cursor.fetchall()
        conn.close()
        
        filename = f"unfriends_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(CSV_FOLDER, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Unfriended_Date'])
            writer.writerows(unfriends)
    
    return send_file(filepath, as_attachment=True)

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM friends WHERE status = 'active'")
    active_friends = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM unfriends")
    total_unfriends = cursor.fetchone()[0]
    
    # Get recent unfriends (last 7 days)
    cursor.execute("""
        SELECT COUNT(*) FROM unfriends 
        WHERE unfriended_date >= datetime('now', '-7 days')
    """)
    recent_unfriends = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'active_friends': active_friends,
        'total_unfriends': total_unfriends,
        'recent_unfriends': recent_unfriends
    })

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Start the web application
    app.run(debug=True, host='0.0.0.0', port=5000)
