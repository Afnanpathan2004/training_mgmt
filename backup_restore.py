import os
import shutil
import datetime
import sqlite3
from pathlib import Path

class BackupRestore:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.backup_dir = self.base_dir / 'backups'
        self.db_path = self.base_dir / 'db.sqlite3'
        self.media_dir = self.base_dir / 'media'
        self.static_dir = self.base_dir / 'static'
        
        # Create backup directory if it doesn't exist
        self.backup_dir.mkdir(exist_ok=True)

    def create_backup(self):
        """Create a backup of the database and important files"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f'backup_{timestamp}'
        backup_path.mkdir(exist_ok=True)

        try:
            # Backup database
            if self.db_path.exists():
                shutil.copy2(self.db_path, backup_path / 'db.sqlite3')
                print(f"Database backed up to {backup_path / 'db.sqlite3'}")

            # Backup media files
            if self.media_dir.exists():
                media_backup = backup_path / 'media'
                shutil.copytree(self.media_dir, media_backup)
                print(f"Media files backed up to {media_backup}")

            # Backup static files
            if self.static_dir.exists():
                static_backup = backup_path / 'static'
                shutil.copytree(self.static_dir, static_backup)
                print(f"Static files backed up to {static_backup}")

            # Create backup info file
            with open(backup_path / 'backup_info.txt', 'w') as f:
                f.write(f"Backup created at: {datetime.datetime.now()}\n")
                f.write(f"Database size: {os.path.getsize(self.db_path) if self.db_path.exists() else 0} bytes\n")
                f.write(f"Media directory size: {self._get_dir_size(self.media_dir) if self.media_dir.exists() else 0} bytes\n")
                f.write(f"Static directory size: {self._get_dir_size(self.static_dir) if self.static_dir.exists() else 0} bytes\n")

            print(f"Backup completed successfully at {backup_path}")
            return backup_path

        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            if backup_path.exists():
                shutil.rmtree(backup_path)
            return None

    def restore_backup(self, backup_path):
        """Restore from a backup"""
        if not os.path.exists(backup_path):
            print(f"Backup path {backup_path} does not exist")
            return False

        try:
            # Restore database
            db_backup = Path(backup_path) / 'db.sqlite3'
            if db_backup.exists():
                shutil.copy2(db_backup, self.db_path)
                print(f"Database restored from {db_backup}")

            # Restore media files
            media_backup = Path(backup_path) / 'media'
            if media_backup.exists():
                if self.media_dir.exists():
                    shutil.rmtree(self.media_dir)
                shutil.copytree(media_backup, self.media_dir)
                print(f"Media files restored from {media_backup}")

            # Restore static files
            static_backup = Path(backup_path) / 'static'
            if static_backup.exists():
                if self.static_dir.exists():
                    shutil.rmtree(self.static_dir)
                shutil.copytree(static_backup, self.static_dir)
                print(f"Static files restored from {static_backup}")

            print(f"Restore completed successfully from {backup_path}")
            return True

        except Exception as e:
            print(f"Error restoring backup: {str(e)}")
            return False

    def list_backups(self):
        """List all available backups"""
        backups = []
        for item in self.backup_dir.iterdir():
            if item.is_dir() and item.name.startswith('backup_'):
                backup_info = {
                    'path': item,
                    'timestamp': item.name.replace('backup_', ''),
                    'size': self._get_dir_size(item)
                }
                backups.append(backup_info)
        return sorted(backups, key=lambda x: x['timestamp'], reverse=True)

    def _get_dir_size(self, path):
        """Calculate total size of a directory"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

def main():
    backup_restore = BackupRestore()
    
    while True:
        print("\nTraining Management System Backup/Restore")
        print("1. Create new backup")
        print("2. List available backups")
        print("3. Restore from backup")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            backup_path = backup_restore.create_backup()
            if backup_path:
                print(f"Backup created at: {backup_path}")
        
        elif choice == '2':
            backups = backup_restore.list_backups()
            if not backups:
                print("No backups found")
            else:
                print("\nAvailable backups:")
                for backup in backups:
                    print(f"Timestamp: {backup['timestamp']}")
                    print(f"Size: {backup['size'] / 1024 / 1024:.2f} MB")
                    print(f"Path: {backup['path']}\n")
        
        elif choice == '3':
            backups = backup_restore.list_backups()
            if not backups:
                print("No backups available to restore from")
                continue
                
            print("\nAvailable backups:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup['timestamp']} ({backup['size'] / 1024 / 1024:.2f} MB)")
            
            try:
                idx = int(input("\nEnter backup number to restore: ")) - 1
                if 0 <= idx < len(backups):
                    if backup_restore.restore_backup(backups[idx]['path']):
                        print("Restore completed successfully")
                    else:
                        print("Restore failed")
                else:
                    print("Invalid backup number")
            except ValueError:
                print("Invalid input")
        
        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main() 