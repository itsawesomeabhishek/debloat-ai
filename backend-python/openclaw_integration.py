"""
OpenClaw Integration Module
Enables chatbot to execute actions via command parsing
"""
import json
import re
from typing import Dict, List, Optional, Tuple
from adb_operations import ADBOperations


class CommandParser:
    """Parse natural language commands into actions"""
    
    def __init__(self):
        self.intent_patterns = {
            'uninstall': [
                re.compile(r'\b(remove|uninstall|delete|get rid of)\s+(.+)'),
                re.compile(r'\b(disable|turn off)\s+(.+)'),
            ],
            'scan': [
                re.compile(r'\b(scan|check|find|show|list)\s+(bloatware|packages|apps)'),
                re.compile(r'what (bloatware|packages|apps)'),
            ],
            'backup': [
                re.compile(r'\b(create|make|backup)\s+(backup|save)'),
            ],
            'restore': [
                re.compile(r'\b(restore|reinstall)\s+(.+)'),
            ],
            'analyze': [
                re.compile(r'\b(analyze|check|tell me about|info about|what is)\s+(.+)'),
            ],
        }
        self.package_pattern = re.compile(r'com\.[a-zA-Z0-9_.]+|[a-z]+\.[a-zA-Z0-9_.]+\.[a-zA-Z0-9_]+')
    
    def parse_command(self, message: str) -> Dict:
        """
        Parse a message and extract intent + entities
        
        Returns:
            {
                'intent': 'uninstall' | 'scan' | 'backup' | 'restore' | 'analyze' | 'chat',
                'entities': {...},
                'confidence': 0.0-1.0,
                'actionable': True/False
            }
        """
        message_lower = message.lower().strip()
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = pattern.search(message_lower)
                if match:
                    entities = self._extract_entities(intent, match, message_lower)
                    return {
                        'intent': intent,
                        'entities': entities,
                        'confidence': 0.8,
                        'actionable': True,
                        'original_message': message
                    }
        
        # No action detected - regular chat
        return {
            'intent': 'chat',
            'entities': {},
            'confidence': 1.0,
            'actionable': False,
            'original_message': message
        }
    
    def _extract_entities(self, intent: str, match: re.Match, message: str) -> Dict:
        """Extract relevant entities based on intent"""
        entities = {}
        
        if intent == 'uninstall':
            target = match.group(2) if len(match.groups()) >= 2 else ''
            entities['target'] = target.strip()
            entities['packages'] = self._extract_package_names(target)
            
        elif intent == 'analyze':
            target = match.group(2) if len(match.groups()) >= 2 else ''
            entities['package'] = target.strip()
            
        elif intent == 'scan':
            entities['type'] = 'bloatware'
            
        elif intent == 'restore':
            target = match.group(2) if len(match.groups()) >= 2 else ''
            entities['package'] = target.strip()
        
        return entities
    
    def _extract_package_names(self, text: str) -> List[str]:
        """Extract potential package names from text"""
        # Check for actual package format (com.example.package)
        packages = self.package_pattern.findall(text)
        
        if packages:
            return packages
        
        # If no package format found, return keywords for fuzzy matching
        return [text]


class ActionExecutor:
    """Execute actions parsed from commands"""
    
    def __init__(self, adb_operations: ADBOperations):
        self.adb = adb_operations
    
    def execute(self, parsed_command: Dict) -> Dict:
        """
        Execute a parsed command
        
        Returns:
            {
                'success': True/False,
                'action': 'uninstall' | 'scan' | etc,
                'requires_confirmation': True/False,
                'data': {...},
                'message': 'Human readable result'
            }
        """
        intent = parsed_command['intent']
        entities = parsed_command['entities']
        
        if intent == 'chat':
            return {
                'success': True,
                'action': 'chat',
                'requires_confirmation': False,
                'data': {},
                'message': 'This is a regular chat message - use AI advisor'
            }
        
        elif intent == 'scan':
            return self._handle_scan(entities)
        
        elif intent == 'uninstall':
            return self._handle_uninstall(entities)
        
        elif intent == 'analyze':
            return self._handle_analyze(entities)
        
        elif intent == 'backup':
            return self._handle_backup(entities)
        
        elif intent == 'restore':
            return self._handle_restore(entities)
        
        return {
            'success': False,
            'action': 'unknown',
            'requires_confirmation': False,
            'data': {},
            'message': f"I don't know how to handle '{intent}' yet"
        }
    
    def _handle_scan(self, entities: Dict) -> Dict:
        """Scan for bloatware packages"""
        try:
            packages = self.adb.list_packages('all')
            
            # Filter for common bloatware patterns
            bloatware = [
                pkg for pkg in packages 
                if self._is_likely_bloatware(pkg['packageName'])
            ]
            
            return {
                'success': True,
                'action': 'scan',
                'requires_confirmation': False,
                'data': {
                    'packages': bloatware,
                    'count': len(bloatware)
                },
                'message': f"Found {len(bloatware)} potential bloatware packages"
            }
        except Exception as e:
            return {
                'success': False,
                'action': 'scan',
                'requires_confirmation': False,
                'data': {},
                'message': f"Scan failed: {str(e)}"
            }
    
    def _handle_uninstall(self, entities: Dict) -> Dict:
        """Handle uninstall request - returns packages for confirmation"""
        target = entities.get('target', '')
        package_names = entities.get('packages', [])
        
        try:
            all_packages = self.adb.list_packages('all')
            
            # Find matching packages
            matches = []

            # Pre-compile regex and set for O(1) and optimized substring matching
            lower_keywords = [k.lower() for k in package_names]
            exact_matches = set(lower_keywords)

            # Only compile regex if there are keywords to prevent empty pattern errors
            if lower_keywords:
                pattern = re.compile('|'.join(re.escape(k) for k in lower_keywords))
            else:
                pattern = None

            for pkg in all_packages:
                pkg_name = pkg['packageName'].lower()
                
                # Direct match (O(1) lookup)
                if pkg_name in exact_matches:
                    matches.append(pkg)
                # Fuzzy match by keywords
                elif pattern and pattern.search(pkg_name):
                    matches.append(pkg)
            
            if not matches:
                return {
                    'success': False,
                    'action': 'uninstall',
                    'requires_confirmation': False,
                    'data': {},
                    'message': f"No packages found matching '{target}'"
                }
            
            return {
                'success': True,
                'action': 'uninstall',
                'requires_confirmation': True,
                'data': {
                    'packages': matches,
                    'count': len(matches)
                },
                'message': f"Found {len(matches)} package(s) to remove. Confirm to proceed."
            }
        except Exception as e:
            return {
                'success': False,
                'action': 'uninstall',
                'requires_confirmation': False,
                'data': {},
                'message': f"Error finding packages: {str(e)}"
            }
    
    def _handle_analyze(self, entities: Dict) -> Dict:
        """Request package analysis"""
        package = entities.get('package', '').strip()
        
        if not package:
            return {
                'success': False,
                'action': 'analyze',
                'requires_confirmation': False,
                'data': {},
                'message': "Please specify a package name to analyze"
            }
        
        return {
            'success': True,
            'action': 'analyze',
            'requires_confirmation': False,
            'data': {'package': package},
            'message': f"Analyzing {package}..."
        }
    
    def _handle_backup(self, entities: Dict) -> Dict:
        """Request backup creation"""
        return {
            'success': True,
            'action': 'backup',
            'requires_confirmation': True,
            'data': {},
            'message': "Creating backup of current packages?"
        }
    
    def _handle_restore(self, entities: Dict) -> Dict:
        """Request package restore"""
        package = entities.get('package', '').strip()
        
        return {
            'success': True,
            'action': 'restore',
            'requires_confirmation': True,
            'data': {'package': package},
            'message': f"Restore {package}?"
        }
    
    def _is_likely_bloatware(self, package_name: str) -> bool:
        """Check if package is likely bloatware"""
        bloatware_indicators = [
            'facebook', 'fb', 'instagram', 'tiktok',
            'netflix', 'spotify', 'amazon',
            'samsung.', 'xiaomi.', 'miui.', 'huawei.',
            'weather', 'news', 'browser',
            'game', 'music', 'video'
        ]
        
        # Don't flag critical system apps
        critical = [
            'com.android.systemui',
            'com.android.phone',
            'com.android.settings',
            'com.google.android.gms'
        ]
        
        if package_name in critical:
            return False
        
        pkg_lower = package_name.lower()
        return any(indicator in pkg_lower for indicator in bloatware_indicators)
    
    def confirm_and_execute(self, action_result: Dict, confirmed: bool) -> Dict:
        """Execute action after user confirmation"""
        if not confirmed:
            return {
                'success': True,
                'message': 'Action cancelled by user'
            }
        
        action = action_result.get('action')
        data = action_result.get('data', {})
        
        if action == 'uninstall':
            return self._execute_uninstall(data.get('packages', []))
        elif action == 'backup':
            return self._execute_backup()
        elif action == 'restore':
            return self._execute_restore(data.get('package'))
        
        return {
            'success': False,
            'message': f"Cannot execute action: {action}"
        }
    
    def _execute_uninstall(self, packages: List[Dict]) -> Dict:
        """Execute actual uninstall"""
        results = []
        success_count = 0
        
        for pkg in packages:
            result = self.adb.uninstall_package(pkg['packageName'])
            results.append({
                'package': pkg['packageName'],
                'success': result.get('success', False),
                'message': result.get('message', '')
            })
            if result.get('success'):
                success_count += 1
        
        return {
            'success': success_count > 0,
            'message': f"Successfully removed {success_count}/{len(packages)} packages",
            'details': results
        }
    
    def _execute_backup(self) -> Dict:
        """Execute backup creation"""
        # This would call backup_manager
        return {
            'success': True,
            'message': 'Backup functionality - integrate with BackupManager'
        }
    
    def _execute_restore(self, package: str) -> Dict:
        """Execute package restore"""
        if not package:
            return {'success': False, 'message': 'No package specified'}
        
        result = self.adb.reinstall_package(package)
        return {
            'success': result.get('success', False),
            'message': result.get('message', 'Restore failed')
        }


class OpenClawIntegration:
    """Main integration class for OpenClaw-powered chatbot"""
    
    def __init__(self, adb_operations: ADBOperations):
        self.parser = CommandParser()
        self.executor = ActionExecutor(adb_operations)
    
    def process_message(self, message: str) -> Dict:
        """
        Process a chat message and determine if action is needed
        
        Returns result dict with action plan or chat response
        """
        # Parse the command
        parsed = self.parser.parse_command(message)
        
        # If it's just chat, return for AI advisor
        if not parsed['actionable']:
            return {
                'type': 'chat',
                'parsed': parsed,
                'execution': None
            }
        
        # Execute the action (may require confirmation)
        execution_result = self.executor.execute(parsed)
        
        return {
            'type': 'action',
            'parsed': parsed,
            'execution': execution_result
        }
    
    def execute_confirmed_action(self, execution_result: Dict, confirmed: bool) -> Dict:
        """Execute an action after user confirmation"""
        return self.executor.confirm_and_execute(execution_result, confirmed)
