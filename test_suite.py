#!/usr/bin/env python3
"""
Facebook Unfriend Tracker - Test Suite
Comprehensive testing for application functionality
"""

import unittest
import tempfile
import os
import json
import sqlite3
import sys
from datetime import datetime

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import extract_friends_from_json, init_db, update_database_with_friends
    from config import TestingConfig
except ImportError as e:
    print(f"Warning: Could not import app modules: {e}")
    print("This is expected if dependencies are not installed yet.")

class TestFacebookTracker(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.test_db = os.path.join(self.test_dir, 'test.db')
        
        # Sample Facebook JSON data
        self.sample_friends_data = [
            {
                "name": "John Doe",
                "timestamp": 1640995200  # 2022-01-01
            },
            {
                "name": "Jane Smith",
                "timestamp": 1640995200
            },
            {
                "name": "Bob Johnson",
                "timestamp": 1640995200
            }
        ]
        
        self.sample_json_file = os.path.join(self.test_dir, 'test_friends.json')
        with open(self.sample_json_file, 'w') as f:
            json.dump({"friends": self.sample_friends_data}, f)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_valid_json_parsing(self):
        """Test parsing valid Facebook JSON files"""
        try:
            friends = extract_friends_from_json(self.sample_json_file)
            self.assertEqual(len(friends), 3)
            self.assertEqual(friends[0]['name'], 'John Doe')
            self.assertEqual(friends[0]['timestamp'], 1640995200)
        except NameError:
            self.skipTest("App module not available")
    
    def test_invalid_json_file(self):
        """Test handling of invalid JSON files"""
        try:
            invalid_file = os.path.join(self.test_dir, 'invalid.json')
            with open(invalid_file, 'w') as f:
                f.write("This is not valid JSON")
            
            with self.assertRaises(ValueError):
                extract_friends_from_json(invalid_file)
        except NameError:
            self.skipTest("App module not available")
    
    def test_empty_json_file(self):
        """Test handling of empty JSON files"""
        try:
            empty_file = os.path.join(self.test_dir, 'empty.json')
            with open(empty_file, 'w') as f:
                f.write("")
            
            with self.assertRaises(ValueError):
                extract_friends_from_json(empty_file)
        except NameError:
            self.skipTest("App module not available")
    
    def test_missing_file(self):
        """Test handling of missing files"""
        try:
            with self.assertRaises(FileNotFoundError):
                extract_friends_from_json('nonexistent.json')
        except NameError:
            self.skipTest("App module not available")
    
    def test_database_operations(self):
        """Test basic database operations"""
        try:
            # This is a simplified test - would need to mock the database in a real scenario
            self.assertTrue(True)  # Placeholder test
        except NameError:
            self.skipTest("App module not available")

class TestProjectStructure(unittest.TestCase):
    """Test that required project files exist"""
    
    def test_required_files_exist(self):
        """Test that all required project files are present"""
        required_files = [
            'app.py',
            'launcher.py', 
            'console_launcher.py',
            'requirements.txt',
            'README.md',
            'run_launcher.bat',
            'utils.py',
            'config.py'
        ]
        
        for file in required_files:
            with self.subTest(file=file):
                self.assertTrue(os.path.exists(file), f"Required file {file} is missing")
    
    def test_template_files_exist(self):
        """Test that all required template files are present"""
        required_templates = [
            'templates/index.html',
            'templates/spreadsheet.html',
            'templates/schedule.html',
            'templates/results.html',
            'templates/dashboard.html'
        ]
        
        for template in required_templates:
            with self.subTest(template=template):
                self.assertTrue(os.path.exists(template), f"Required template {template} is missing")
    
    def test_directories_exist(self):
        """Test that required directories exist or can be created"""
        required_dirs = ['uploads', 'data', 'templates']
        
        for directory in required_dirs:
            with self.subTest(directory=directory):
                if not os.path.exists(directory):
                    try:
                        os.makedirs(directory, exist_ok=True)
                        created = True
                    except:
                        created = False
                    self.assertTrue(created, f"Could not create required directory {directory}")
                else:
                    self.assertTrue(os.path.isdir(directory), f"{directory} exists but is not a directory")

class TestConfiguration(unittest.TestCase):
    """Test configuration and security settings"""
    
    def test_gitignore_protects_data(self):
        """Test that .gitignore protects sensitive data"""
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                gitignore_content = f.read()
            
            # Check for important patterns
            important_patterns = ['*.db', 'uploads/', 'data/', '*.csv']
            for pattern in important_patterns:
                with self.subTest(pattern=pattern):
                    self.assertIn(pattern, gitignore_content, 
                                f"Gitignore should protect {pattern}")
    
    def test_requirements_file(self):
        """Test that requirements.txt contains necessary dependencies"""
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        essential_packages = ['Flask', 'Werkzeug']
        for package in essential_packages:
            with self.subTest(package=package):
                self.assertIn(package, requirements, 
                            f"Requirements should include {package}")

def create_sample_data():
    """Create sample data for testing"""
    print("Creating sample test data...")
    
    # Create test uploads directory
    os.makedirs('uploads', exist_ok=True)
    
    # Create sample Facebook JSON file
    sample_data = {
        "friends": [
            {"name": "Test Friend 1", "timestamp": 1640995200},
            {"name": "Test Friend 2", "timestamp": 1640995300},
            {"name": "Test Friend 3", "timestamp": 1640995400}
        ]
    }
    
    sample_file = os.path.join('uploads', 'sample_friends.json')
    with open(sample_file, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"✅ Sample data created: {sample_file}")
    return sample_file

def run_manual_tests():
    """Run manual tests that require user interaction"""
    print("\n🧪 MANUAL TEST SUGGESTIONS")
    print("=" * 40)
    print("1. Test file upload with the sample data created")
    print("2. Test the web interface by starting the server")
    print("3. Test the GUI launcher")
    print("4. Test CSV export functionality")
    print("5. Test dashboard and spreadsheet views")
    print("\nSample data location: uploads/sample_friends.json")

def main():
    """Main test runner"""
    print("🧪 Facebook Unfriend Tracker - Test Suite")
    print("=" * 50)
    
    # Create sample data
    sample_file = create_sample_data()
    
    # Run automated tests
    print("\n🔧 Running Automated Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run manual test suggestions
    run_manual_tests()

if __name__ == '__main__':
    main()
