#!/usr/bin/env python
"""
QabiFly Migration Script
Run all migrations for the new QabiFly apps
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            print(result.stdout)
        else:
            print(f"❌ {description} - FAILED")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False
    return True

def main():
    """Main migration function"""
    print("🚀 QabiFly Migration Script")
    print("=" * 50)
    
    # List of all migration commands
    migrations = [
        ("khata", "Create Khata (Digital Udhaar) tables"),
        ("wallet", "Create Wallet tables"),
        ("delivery", "Create Delivery system tables"),
        ("notifications", "Create Notifications tables"),
        ("weather", "Create Weather & IoT tables"),
        ("kyc", "Create KYC tables"),
        ("emi", "Create EMI system tables"),
        ("support", "Create Chat Support tables"),
        ("videos", "Create Video Content tables"),
        ("gismap", "Create GIS Map tables"),
        ("medical", "Create Medical stub tables"),
        ("education", "Create Education stub tables"),
    ]
    
    # Run all migrations
    all_success = True
    for app, description in migrations:
        cmd = f"python manage.py makemigrations {app}"
        success = run_command(cmd, description)
        if not success:
            all_success = False
    
    # Run the final migrate command
    if all_success:
        print("\n" + "=" * 50)
        print("🔄 Running final migration...")
        cmd = "python manage.py migrate"
        success = run_command(cmd, description="Final Migration")
        
        if success:
            print("\n" + "=" * 50)
            print("🎉 QabiFly Migration Completed Successfully!")
            print("📝 All apps have been migrated and are ready for use.")
            print("\n📋 Next Steps:")
            print("1. Run 'python manage.py createsuperuser' to create admin user")
            print("2. Start the development server with 'python manage.py runserver'")
            print("3. Access the API at http://127.0.0.1:8000/graphql/")
            print("4. Check the admin panel at http://127.0.0.1:8000/admin/")
        else:
            print("\n" + "=" * 50)
            print("❌ Migration failed. Please check the errors above.")
            sys.exit(1)
    else:
        print("\n" + "=" * 50)
        print("❌ Migration failed due to errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
