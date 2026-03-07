"""
Backup Manager Module
Handles backup and restore of uninstalled packages
"""
import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path


class BackupManager:
    """Manage backups of uninstalled packages"""
    
    def __init__(self, backup_dir: str = None):
        """Initialize backup manager"""
        if backup_dir is None:
            # Use user's documents folder
            home = Path.home()
            self.backup_dir = home / "DebloatAI" / "backups"
        else:
            self.backup_dir = Path(backup_dir)
        
        # Create backup directory if it doesn't exist
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, packages: List[str], device_info: Dict = None) -> Dict:
        """Create a backup of packages"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.json"
            backup_path = self.backup_dir / backup_name
            
            backup_data = {
                "timestamp": datetime.now().isoformat(),
                "deviceInfo": device_info or {},
                "packages": packages,
                "count": len(packages)
            }
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            return {
                "success": True,
                "backupName": backup_name,
                "backupPath": str(backup_path),
                "message": f"Backup created: {backup_name}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create backup: {str(e)}"
            }
    
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        try:
            backups = []
            
            for backup_file in self.backup_dir.glob("backup_*.json"):
                try:
                    with open(backup_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    backups.append({
                        "name": backup_file.name,
                        "path": str(backup_file),
                        "timestamp": data.get("timestamp", ""),
                        "packageCount": data.get("count", 0),
                        "deviceInfo": data.get("deviceInfo", {})
                    })
                except:
                    # Skip corrupted backup files
                    continue
            
            # Sort by timestamp (newest first)
            backups.sort(key=lambda x: x["timestamp"], reverse=True)
            
            return backups
            
        except Exception as e:
            raise Exception(f"Failed to list backups: {str(e)}")
    
    def restore_backup(self, backup_name: str) -> Dict:
        """Restore packages from a backup"""
        try:
            backup_path = self._get_safe_backup_path(backup_name)
            
            if not backup_path.exists():
                return {
                    "success": False,
                    "message": f"Backup not found: {backup_name}"
                }
            
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            packages = backup_data.get("packages", [])
            
            return {
                "success": True,
                "packages": packages,
                "count": len(packages),
                "message": f"Loaded {len(packages)} packages from backup"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to restore backup: {str(e)}"
            }
    
    def delete_backup(self, backup_name: str) -> Dict:
        """Delete a backup file"""
        try:
            backup_path = self._get_safe_backup_path(backup_name)
            
            if not backup_path.exists():
                return {
                    "success": False,
                    "message": f"Backup not found: {backup_name}"
                }
            
            backup_path.unlink()
            
            return {
                "success": True,
                "message": f"Deleted backup: {backup_name}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to delete backup: {str(e)}"
            }
    
    def _get_safe_backup_path(self, backup_name: str) -> Path:
        """
        Sanitize and validate backup name to prevent path traversal.
        Only allows files within the backup directory.
        """
        # Take only the filename part to prevent directory traversal
        safe_name = Path(backup_name).name
        target_path = (self.backup_dir / safe_name).resolve()

        # Verify the path is still within backup_dir
        if not target_path.is_relative_to(self.backup_dir.resolve()):
            raise ValueError(f"Invalid backup name: {backup_name}")

        return target_path

    def get_backup_path(self) -> str:
        """Get the backup directory path"""
        return str(self.backup_dir)
