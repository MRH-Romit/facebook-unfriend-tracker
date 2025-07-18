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
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Create friends table with improved schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS friends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                facebook_timestamp INTEGER DEFAULT 0,
                first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name) ON CONFLICT REPLACE
            )
        ''')
        
        # Create unfriends table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS unfriends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                unfriended_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_seen DATETIME,
                friend_duration_days INTEGER DEFAULT 0
            )
        ''')
        
        # Create tracking_history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracking_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_friends INTEGER,
                unfriended_count INTEGER,
                new_friends_count INTEGER,
                check_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                upload_filename TEXT
            )
        ''')
        
        # Create application_log table for better logging
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS application_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_action TEXT
            )
        ''')
        
        conn.commit()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        if conn:
            conn.close()
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

def log_action(level, message, user_action=None):
    """Log application events to database"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO application_log (level, message, user_action) 
            VALUES (?, ?, ?)
        ''', (level, message, user_action))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to log action: {e}")
    finally:
        if conn:
            conn.close()

def allowed_file(filename):
    """Check if uploaded file has allowed extension and is safe"""
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return False
        
    # Additional security checks
    if len(filename) > 255:  # Prevent extremely long filenames
        return False
        
    # Check for dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
    if any(char in filename for char in dangerous_chars):
        return False
        
    return True

def extract_friends_from_json(file_path):
    """Extract friends list from Facebook JSON file with improved error handling"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    if os.path.getsize(file_path) == 0:
        raise ValueError("File is empty")
        
    if os.path.getsize(file_path) > 50 * 1024 * 1024:  # 50MB limit
        raise ValueError("File too large (max 50MB)")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON file: {e}")
        raise ValueError("Invalid JSON format. Please ensure you uploaded a valid Facebook JSON file.")
    except UnicodeDecodeError as e:
        logger.error(f"Encoding error: {e}")
        raise ValueError("File encoding error. Please ensure the file is properly encoded.")
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise ValueError(f"Error reading file: {str(e)}")
            
    # Handle different possible structures with validation
    friends = []
    
    try:
        if isinstance(data, dict):
            if 'friends' in data:
                friends = data['friends']
            elif 'friends_v2' in data:
                friends = data['friends_v2']
            elif 'data' in data:
                friends = data['data']
            else:
                # Check if the data itself contains friend information
                if 'name' in data or 'display_name' in data:
                    friends = [data]
                else:
                    raise ValueError("Unrecognized Facebook JSON structure")
        elif isinstance(data, list):
            friends = data
        else:
            raise ValueError("Invalid JSON structure. Expected object or array.")
            
        if not friends:
            raise ValueError("No friends data found in the file")
            
        # Extract names and timestamps with validation
        friend_data = []
        processed_names = set()  # Prevent duplicates
        
        for idx, friend in enumerate(friends):
            try:
                if isinstance(friend, dict):
                    name = friend.get('name', '')
                    if not name:
                        # Try other possible keys
                        name = (friend.get('display_name', '') or 
                               friend.get('full_name', '') or 
                               friend.get('title', ''))
                    
                    if not name or not isinstance(name, str):
                        logger.warning(f"Skipping friend entry {idx}: no valid name found")
                        continue
                        
                    name = name.strip()
                    if not name or len(name) > 255:  # Reasonable name length limit
                        logger.warning(f"Skipping friend entry {idx}: invalid name")
                        continue
                        
                    # Skip duplicates
                    if name in processed_names:
                        logger.warning(f"Skipping duplicate friend: {name}")
                        continue
                    processed_names.add(name)
                    
                    timestamp = friend.get('timestamp', 0)
                    
                    # Validate and convert timestamp
                    if timestamp:
                        try:
                            if isinstance(timestamp, str):
                                timestamp = int(timestamp)
                            friend_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                        except (ValueError, OverflowError, OSError):
                            logger.warning(f"Invalid timestamp for {name}: {timestamp}")
                            friend_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            timestamp = 0
                    else:
                        friend_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        timestamp = 0
                    
                    friend_data.append({
                        'name': name,
                        'timestamp': timestamp,
                        'date_added': friend_date
                    })
                    
                elif isinstance(friend, str):
                    name = friend.strip()
                    if name and len(name) <= 255 and name not in processed_names:
                        processed_names.add(name)
                        friend_data.append({
                            'name': name,
                            'timestamp': 0,
                            'date_added': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                else:
                    logger.warning(f"Skipping invalid friend entry {idx}: {type(friend)}")
                    
            except Exception as e:
                logger.warning(f"Error processing friend entry {idx}: {e}")
                continue
                
        if not friend_data:
            raise ValueError("No valid friends found in the file. Please check the file format.")
            
        logger.info(f"Successfully extracted {len(friend_data)} friends from JSON")
        return friend_data
        
    except Exception as e:
        logger.error(f"Error extracting friends: {e}")
        if isinstance(e, ValueError):
            raise
        else:
            raise ValueError(f"Error processing friends data: {str(e)}")

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

def update_database_with_friends(friends_data, upload_filename=None):
    """Update database with current friends data"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # Get current friends from database
        cursor.execute("SELECT name FROM friends WHERE status = 'active'")
        current_friends = set(row[0] for row in cursor.fetchall())
        
        new_friends = set(friend['name'] for friend in friends_data)
        
        # Find unfriended users
        unfriended = current_friends - new_friends
        
        # Find new friends
        newly_added = new_friends - current_friends
        
        current_time = datetime.now()
        
        # Mark unfriended users as inactive
        for friend in unfriended:
            cursor.execute("""
                UPDATE friends SET status = 'inactive', last_updated = ? 
                WHERE name = ? AND status = 'active'
            """, (current_time, friend))
            
            # Calculate friendship duration
            cursor.execute("""
                SELECT first_seen FROM friends WHERE name = ? AND status = 'inactive'
            """, (friend,))
            result = cursor.fetchone()
            
            friendship_duration = 0
            if result and result[0]:
                try:
                    first_seen = datetime.fromisoformat(result[0])
                    friendship_duration = (current_time - first_seen).days
                except:
                    friendship_duration = 0
            
            # Add to unfriends table
            cursor.execute("""
                INSERT INTO unfriends (name, unfriended_date, friend_duration_days) 
                VALUES (?, ?, ?)
            """, (friend, current_time, friendship_duration))
        
        # Add new friends with their original Facebook timestamp
        for friend in friends_data:
            if friend['name'] in newly_added:
                cursor.execute("""
                    INSERT OR REPLACE INTO friends 
                    (name, timestamp, status, facebook_timestamp, first_seen, last_updated) 
                    VALUES (?, ?, 'active', ?, ?, ?)
                """, (friend['name'], current_time, friend['timestamp'], current_time, current_time))
            else:
                # Update existing friends' last_updated timestamp
                cursor.execute("""
                    UPDATE friends SET last_updated = ? WHERE name = ? AND status = 'active'
                """, (current_time, friend['name']))
        
        # Update tracking history
        cursor.execute("""
            INSERT INTO tracking_history 
            (total_friends, unfriended_count, new_friends_count, upload_filename)
            VALUES (?, ?, ?, ?)
        """, (len(new_friends), len(unfriended), len(newly_added), upload_filename))
        
        conn.commit()
        logger.info(f"Database updated: {len(new_friends)} total, {len(unfriended)} unfriended, {len(newly_added)} new")
        
        return list(unfriended), list(newly_added)
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Database update failed: {e}")
        raise
    finally:
        conn.close()

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

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    flash('An internal error occurred. Please try again.')
    return render_template('index.html'), 500

@app.errorhandler(RequestEntityTooLarge)
def too_large(error):
    """Handle file too large errors"""
    flash('File too large. Maximum size is 16MB.')
    return redirect(url_for('index')), 413

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
    """Handle file upload with improved validation and error handling"""
    try:
        if 'file' not in request.files:
            flash('No file selected')
            log_action('WARNING', 'Upload attempted without file', 'file_upload')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            log_action('WARNING', 'Upload attempted with empty filename', 'file_upload')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload a JSON file.')
            log_action('WARNING', f'Invalid file type attempted: {file.filename}', 'file_upload')
            return redirect(url_for('index'))
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        if not filename:
            flash('Invalid filename. Please rename your file and try again.')
            return redirect(url_for('index'))
            
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Add timestamp to prevent overwrites
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filename = f"{base}_{counter}{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            counter += 1
        
        file.save(filepath)
        log_action('INFO', f'File uploaded successfully: {filename}', 'file_upload')
        
        # Extract friends with error handling
        try:
            friends_data = extract_friends_from_json(filepath)
        except (ValueError, FileNotFoundError) as e:
            # Clean up uploaded file on error
            try:
                os.remove(filepath)
            except:
                pass
            flash(str(e))
            log_action('ERROR', f'File processing failed: {str(e)}', 'file_processing')
            return redirect(url_for('index'))
        
        if not friends_data:
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except:
                pass
            flash('Could not extract friends from the file. Please check the file format.')
            log_action('ERROR', 'No friends data extracted from file', 'file_processing')
            return redirect(url_for('index'))
        
        # Save to CSV
        try:
            csv_filepath = save_friends_to_csv(friends_data, f"{base}_processed.csv")
        except Exception as e:
            logger.error(f"Failed to save CSV: {e}")
            flash('Warning: Could not save CSV backup.')
            csv_filepath = None
        
        # Update database and get changes
        try:
            unfriended, newly_added = update_database_with_friends(friends_data, filename)
        except Exception as e:
            logger.error(f"Database update failed: {e}")
            flash('Error updating database. Please try again.')
            log_action('ERROR', f'Database update failed: {str(e)}', 'database_update')
            return redirect(url_for('index'))
        
        # Save unfriends to CSV if any
        if unfriended:
            try:
                save_unfriends_to_csv(unfriended)
            except Exception as e:
                logger.error(f"Failed to save unfriends CSV: {e}")
        
        success_msg = f'Successfully processed {len(friends_data)} friends. Found {len(unfriended)} unfriends and {len(newly_added)} new friends.'
        flash(success_msg)
        log_action('INFO', success_msg, 'processing_complete')
        
        return render_template('results.html', 
                             total_friends=len(friends_data),
                             unfriended=unfriended,
                             newly_added=newly_added,
                             csv_path=csv_filepath)
    
    except Exception as e:
        logger.error(f"Unexpected error in upload: {e}")
        flash('An unexpected error occurred. Please try again.')
        log_action('ERROR', f'Unexpected upload error: {str(e)}', 'file_upload')
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
