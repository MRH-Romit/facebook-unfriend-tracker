#!/usr/bin/env python3
"""
Facebook Unfriend Tracker - Utility Management Script
Provides maintenance, backup, and cleanup functions
"""

import os
import sqlite3
import json
import csv
import shutil
import sys
from datetime import datetime, timedelta
import argparse

class TrackerUtilities:
    def __init__(self, database_path='friends_tracker.db'):
        self.database_path = database_path
        self.backup_dir = 'backups'
        
    def create_backup(self):
        """Create a complete backup of the database and data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_folder = os.path.join(self.backup_dir, f'backup_{timestamp}')
        
        os.makedirs(backup_folder, exist_ok=True)
        
        # Backup database
        if os.path.exists(self.database_path):
            shutil.copy2(self.database_path, 
                        os.path.join(backup_folder, f'friends_tracker_backup_{timestamp}.db'))
            
        # Backup data folder
        if os.path.exists('data'):
            shutil.copytree('data', os.path.join(backup_folder, 'data'), dirs_exist_ok=True)
            
        # Create backup manifest
        manifest = {
            'backup_date': datetime.now().isoformat(),
            'files_backed_up': os.listdir(backup_folder),
            'backup_type': 'full',
            'database_size': os.path.getsize(self.database_path) if os.path.exists(self.database_path) else 0
        }
        
        with open(os.path.join(backup_folder, 'manifest.json'), 'w') as f:
            json.dump(manifest, f, indent=2)
            
        print(f"✅ Backup created: {backup_folder}")
        return backup_folder
        
    def clean_old_backups(self, keep_days=30):
        """Remove backups older than specified days"""
        if not os.path.exists(self.backup_dir):
            return
            
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        removed_count = 0
        
        for backup_folder in os.listdir(self.backup_dir):
            backup_path = os.path.join(self.backup_dir, backup_folder)
            if os.path.isdir(backup_path):
                try:
                    # Extract date from folder name
                    if backup_folder.startswith('backup_'):
                        date_str = backup_folder.replace('backup_', '')[:15]  # YYYYMMDD_HHMMSS
                        backup_date = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
                        
                        if backup_date < cutoff_date:
                            shutil.rmtree(backup_path)
                            removed_count += 1
                            print(f"🗑️  Removed old backup: {backup_folder}")
                except Exception as e:
                    print(f"⚠️  Could not process backup {backup_folder}: {e}")
                    
        print(f"✅ Cleaned {removed_count} old backups")
        
    def get_database_stats(self):
        """Get comprehensive database statistics"""
        if not os.path.exists(self.database_path):
            print("❌ Database not found")
            return
            
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        
        try:
            # Friends statistics
            cursor.execute("SELECT COUNT(*) FROM friends WHERE status = 'active'")
            active_friends = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM friends WHERE status = 'inactive'")
            inactive_friends = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM unfriends")
            total_unfriends = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tracking_history")
            total_uploads = cursor.fetchone()[0]
            
            # Recent activity
            cursor.execute("""
                SELECT COUNT(*) FROM unfriends 
                WHERE unfriended_date >= datetime('now', '-7 days')
            """)
            recent_unfriends = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM unfriends 
                WHERE unfriended_date >= datetime('now', '-30 days')
            """)
            monthly_unfriends = cursor.fetchone()[0]
            
            # Database size
            db_size = os.path.getsize(self.database_path)
            
            # First and last activity
            cursor.execute("SELECT MIN(check_date), MAX(check_date) FROM tracking_history")
            date_range = cursor.fetchone()
            
            print("\n📊 DATABASE STATISTICS")
            print("=" * 50)
            print(f"Active Friends: {active_friends}")
            print(f"Inactive Friends: {inactive_friends}")
            print(f"Total Friends Ever: {active_friends + inactive_friends}")
            print(f"Total Unfriends: {total_unfriends}")
            print(f"Data Uploads: {total_uploads}")
            print(f"Recent Unfriends (7 days): {recent_unfriends}")
            print(f"Recent Unfriends (30 days): {monthly_unfriends}")
            print(f"Database Size: {db_size / 1024:.1f} KB")
            
            if date_range[0] and date_range[1]:
                print(f"First Upload: {date_range[0][:10]}")
                print(f"Last Upload: {date_range[1][:10]}")
                
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
        finally:
            conn.close()
            
    def export_all_data(self):
        """Export all data to CSV files"""
        if not os.path.exists(self.database_path):
            print("❌ Database not found")
            return
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_dir = f'export_{timestamp}'
        os.makedirs(export_dir, exist_ok=True)
        
        conn = sqlite3.connect(self.database_path)
        
        try:
            # Export friends
            with open(os.path.join(export_dir, 'all_friends.csv'), 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                cursor = conn.execute("""
                    SELECT name, status, timestamp, facebook_timestamp, first_seen, last_updated 
                    FROM friends ORDER BY name
                """)
                writer.writerow(['Name', 'Status', 'Tracked_Date', 'Facebook_Timestamp', 'First_Seen', 'Last_Updated'])
                writer.writerows(cursor.fetchall())
                
            # Export unfriends
            with open(os.path.join(export_dir, 'all_unfriends.csv'), 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                cursor = conn.execute("""
                    SELECT name, unfriended_date, friend_duration_days 
                    FROM unfriends ORDER BY unfriended_date DESC
                """)
                writer.writerow(['Name', 'Unfriended_Date', 'Friendship_Duration_Days'])
                writer.writerows(cursor.fetchall())
                
            # Export tracking history
            with open(os.path.join(export_dir, 'tracking_history.csv'), 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                cursor = conn.execute("""
                    SELECT check_date, total_friends, unfriended_count, new_friends_count, upload_filename 
                    FROM tracking_history ORDER BY check_date DESC
                """)
                writer.writerow(['Check_Date', 'Total_Friends', 'Unfriended_Count', 'New_Friends_Count', 'Upload_Filename'])
                writer.writerows(cursor.fetchall())
                
            print(f"✅ All data exported to: {export_dir}")
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
        finally:
            conn.close()
            
    def cleanup_temp_files(self):
        """Clean up temporary files and old uploads"""
        removed_count = 0
        
        # Clean uploads folder of old files (keep only recent ones)
        if os.path.exists('uploads'):
            cutoff_time = datetime.now() - timedelta(days=7)
            
            for filename in os.listdir('uploads'):
                filepath = os.path.join('uploads', filename)
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if file_time < cutoff_time:
                        try:
                            os.remove(filepath)
                            removed_count += 1
                            print(f"🗑️  Removed old upload: {filename}")
                        except Exception as e:
                            print(f"⚠️  Could not remove {filename}: {e}")
                            
        # Clean Python cache files
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith(('.pyc', '.pyo')) or file.startswith('.DS_Store'):
                    try:
                        os.remove(os.path.join(root, file))
                        removed_count += 1
                    except:
                        pass
                        
            # Remove __pycache__ directories
            if '__pycache__' in dirs:
                try:
                    shutil.rmtree(os.path.join(root, '__pycache__'))
                    removed_count += 1
                except:
                    pass
                    
        print(f"✅ Cleaned {removed_count} temporary files")
        
    def check_integrity(self):
        """Check database integrity and consistency"""
        if not os.path.exists(self.database_path):
            print("❌ Database not found")
            return False
            
        conn = sqlite3.connect(self.database_path)
        
        try:
            # Basic integrity check
            cursor = conn.execute("PRAGMA integrity_check")
            integrity_result = cursor.fetchone()[0]
            
            if integrity_result != 'ok':
                print(f"❌ Database integrity check failed: {integrity_result}")
                return False
                
            # Check for orphaned records
            cursor = conn.execute("""
                SELECT COUNT(*) FROM unfriends u 
                WHERE NOT EXISTS (SELECT 1 FROM friends f WHERE f.name = u.name)
            """)
            orphaned_unfriends = cursor.fetchone()[0]
            
            if orphaned_unfriends > 0:
                print(f"⚠️  Found {orphaned_unfriends} orphaned unfriend records")
                
            print("✅ Database integrity check passed")
            return True
            
        except Exception as e:
            print(f"❌ Integrity check failed: {e}")
            return False
        finally:
            conn.close()

def main():
    parser = argparse.ArgumentParser(description='Facebook Unfriend Tracker Utilities')
    parser.add_argument('action', choices=['backup', 'stats', 'export', 'cleanup', 'integrity', 'clean-backups'],
                       help='Action to perform')
    parser.add_argument('--days', type=int, default=30, help='Number of days for cleanup operations')
    
    args = parser.parse_args()
    
    utils = TrackerUtilities()
    
    if args.action == 'backup':
        utils.create_backup()
    elif args.action == 'stats':
        utils.get_database_stats()
    elif args.action == 'export':
        utils.export_all_data()
    elif args.action == 'cleanup':
        utils.cleanup_temp_files()
    elif args.action == 'integrity':
        utils.check_integrity()
    elif args.action == 'clean-backups':
        utils.clean_old_backups(args.days)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("\n🔧 Facebook Unfriend Tracker Utilities")
        print("=" * 40)
        print("Available commands:")
        print("  python utils.py backup        - Create backup")
        print("  python utils.py stats         - Show database stats")
        print("  python utils.py export        - Export all data to CSV")
        print("  python utils.py cleanup       - Clean temporary files")
        print("  python utils.py integrity     - Check database integrity")
        print("  python utils.py clean-backups - Remove old backups")
        print("\nFor help: python utils.py -h")
    else:
        main()
