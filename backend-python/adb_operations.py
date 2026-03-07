"""
ADB Operations Module
Handles all Android Debug Bridge operations
"""
import subprocess
import json
from typing import List, Dict, Optional
import re


class ADBError(Exception):
    """Custom exception for ADB errors"""
    pass


class ADBOperations:
    """Handle all ADB-related operations"""
    
    @staticmethod
    def is_valid_package_name(package_name: str) -> bool:
        """Validate Android package name format to prevent injection attacks"""
        if not package_name:
            return False
        # Standard Android package name format
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)*$'
        return bool(re.match(pattern, package_name))

    def __init__(self):
        import shutil
        import os
        import sys
        
        # Determine base directory (PyInstaller exe or script location)
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Search priority:
        # 1. Bundled platform-tools next to exe (production)
        # 2. System PATH
        # 3. Common Windows install location
        bundled = os.path.join(base_dir, 'platform-tools', 'adb.exe')
        if os.path.exists(bundled):
            self.adb_path = bundled
        elif shutil.which('adb'):
            self.adb_path = shutil.which('adb')
        elif os.path.exists(r'C:\platform-tools\adb.exe'):
            self.adb_path = r'C:\platform-tools\adb.exe'
        else:
            self.adb_path = 'adb'
    
    def _run_command(self, command: List[str], timeout: int = 30) -> str:
        """Run an ADB command and return output"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                
                # Parse common ADB errors
                if "no devices found" in error_msg.lower():
                    raise ADBError("No Android device connected. Please connect via USB.")
                elif "device unauthorized" in error_msg.lower():
                    raise ADBError("Device unauthorized. Please check device for USB debugging prompt.")
                elif "device offline" in error_msg.lower():
                    raise ADBError("Device is offline. Please reconnect the device.")
                else:
                    raise ADBError(f"ADB command failed: {error_msg}")
            
            return result.stdout
            
        except subprocess.TimeoutExpired:
            raise ADBError("ADB command timed out. Please check device connection.")
        except FileNotFoundError:
            raise ADBError("ADB not found. Please install Android SDK Platform Tools.")
    
    def get_device_info(self) -> Dict:
        """Get information about connected Android device"""
        try:
            # Get device serial
            devices = self._run_command([self.adb_path, "devices", "-l"])
            lines = [l for l in devices.split('\n') if l.strip() and not l.startswith('List')]
            
            if not lines:
                raise ADBError("No device connected")
            
            # Parse first device
            device_line = lines[0]
            parts = device_line.split()
            serial = parts[0]
            
            # Get device properties
            model = self._get_property("ro.product.model")
            product = self._get_property("ro.product.name")
            manufacturer = self._get_property("ro.product.manufacturer")
            android_version = self._get_property("ro.build.version.release")
            
            return {
                "name": serial,
                "serial": serial,
                "model": model,
                "product": product,
                "manufacturer": manufacturer,
                "androidVersion": android_version,
                "state": "device"
            }
        except Exception as e:
            raise ADBError(str(e))
    
    def _get_property(self, prop: str) -> str:
        """Get a device property"""
        try:
            output = self._run_command([self.adb_path, "shell", "getprop", prop])
            return output.strip()
        except:
            return "Unknown"
    
    def list_packages(self, package_type: str = "all") -> List[Dict]:
        """List installed packages on device"""
        try:
            # Get package list
            if package_type == "system":
                cmd = [self.adb_path, "shell", "pm", "list", "packages", "-s"]
            elif package_type == "user":
                cmd = [self.adb_path, "shell", "pm", "list", "packages", "-3"]
            else:
                cmd = [self.adb_path, "shell", "pm", "list", "packages"]
            
            output = self._run_command(cmd)
            
            packages = []
            for line in output.split('\n'):
                if line.startswith('package:'):
                    package_name = line.replace('package:', '').strip()
                    if package_name:
                        packages.append({
                            "packageName": package_name,
                            "appName": self._get_app_name(package_name),
                            "safetyLevel": self._determine_safety_level(package_name)
                        })
            
            # Sort by package name
            packages.sort(key=lambda p: p["packageName"])
            
            return packages
            
        except Exception as e:
            raise ADBError(f"Failed to list packages: {str(e)}")
    
    def _guess_package_type(self, package: str) -> str:
        """Guess if package is system or user app"""
        system_prefixes = [
            'com.android.',
            'com.google.',
            'com.samsung.',
            'com.xiaomi.',
            'com.huawei.',
            'com.oppo.',
            'com.vivo.',
            'android.'
        ]
        
        for prefix in system_prefixes:
            if package.startswith(prefix):
                return "system"
        return "user"
    
    def _get_app_name(self, package_name: str) -> str:
        """Extract a friendly app name from package name"""
        # Remove common prefixes
        name = package_name
        prefixes = ['com.android.', 'com.google.', 'com.', 'org.', 'net.']
        for prefix in prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        
        # Split by dots and take the most relevant part
        parts = name.split('.')
        if parts:
            name = parts[0]
        
        # Capitalize first letter
        return name.capitalize()
    
    def _determine_safety_level(self, package_name: str) -> str:
        """Determine safety level for removing a package"""
        # Dangerous - Critical system apps
        dangerous_packages = {
            'com.android.systemui',
            'com.android.phone',
            'com.android.settings',
            'com.android.launcher',
            'com.android.launcher3',
            'com.android.vending',  # Play Store
        }
        
        # Expert - May break functionality
        expert_prefixes = [
            'com.google.android.gms',  # Google Play Services
            'com.google.android.gsf',  # Google Services Framework
            'com.android.bluetooth',
            'com.android.nfc',
        ]
        
        # Caution - OEM apps
        caution_prefixes = [
            'com.samsung.',
            'com.xiaomi.',
            'com.miui.',
            'com.huawei.',
            'com.oppo.',
            'com.vivo.',
            'com.realme.',
            'com.oneplus.',
        ]
        
        # Check dangerous
        if package_name in dangerous_packages:
            return "Dangerous"
        
        # Check expert
        for prefix in expert_prefixes:
            if package_name.startswith(prefix):
                return "Expert"
        
        # Check caution
        for prefix in caution_prefixes:
            if package_name.startswith(prefix):
                return "Caution"
        
        # Default to Safe (user apps, bloatware)
        return "Safe"
    
    def uninstall_package(self, package_name: str) -> Dict:
        """Uninstall a package from device"""
        if not self.is_valid_package_name(package_name):
            return {
                "success": False,
                "message": f"Invalid package name format: {package_name}"
            }

        try:
            # Try uninstall
            output = self._run_command(
                [self.adb_path, "shell", "pm", "uninstall", "--user", "0", package_name]
            )
            
            if "Success" in output:
                return {
                    "success": True,
                    "message": f"Successfully uninstalled {package_name}"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to uninstall: {output.strip()}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }
    
    def reinstall_package(self, package_name: str) -> Dict:
        """Reinstall a previously removed package"""
        if not self.is_valid_package_name(package_name):
            return {
                "success": False,
                "message": f"Invalid package name format: {package_name}"
            }

        try:
            # Reinstall for user 0
            output = self._run_command(
                [self.adb_path, "shell", "cmd", "package", "install-existing", package_name]
            )
            
            if "installed" in output.lower():
                return {
                    "success": True,
                    "message": f"Successfully reinstalled {package_name}"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to reinstall: {output.strip()}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }
