"""
Gmail Watcher - Monitors Gmail for urgent/important messages
Silver Tier Implementation

Uses credentials.json from the credentials folder
"""
from pathlib import Path
from datetime import datetime
import logging
import os
import base64
from email import message_from_bytes

class GmailWatcher:
    def __init__(self, vault_path: str, check_interval: int = 120, credentials_file: str = "credentials.json"):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval  # Check every 2 minutes
        self.processed_ids = set()
        self.keywords = [
            'urgent', 'asap', 'invoice', 'payment', 'help',
            'deadline', 'important', 'action required', 'reply needed',
            'quotation', 'proposal', 'meeting', 'call'
        ]
        
        # Credentials path - looks in project root credentials folder
        # Project root is parent of AI_Employee_Vault
        self.project_root = self.vault_path.parent
        self.credentials_dir = self.project_root / 'credentials'
        self.credentials_file = self.credentials_dir / credentials_file
        self.token_file = self.credentials_dir / 'gmail-token.json'
        
        # Setup logging
        self.logger = logging.getLogger('GmailWatcher')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.vault_path / 'Logs' / 'gmail_watcher.log'),
                logging.StreamHandler()
            ]
        )
        
        # Try to import Gmail API libraries
        try:
            from google.oauth2.credentials import Credentials
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            from google.auth.transport.requests import Request
            self.google_available = True
        except ImportError:
            self.google_available = False
            self.logger.error("Google API libraries not installed!")
            self.logger.error("Run: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        
        self.service = None
        
    def authenticate(self):
        """Authenticate with Gmail API using credentials.json"""
        if not self.google_available:
            self.logger.error("Google API libraries not available")
            return False
        
        # Check if credentials file exists
        if not self.credentials_file.exists():
            self.logger.error(f"Credentials file not found: {self.credentials_file}")
            self.logger.error("Please place your credentials.json file in AI_Employee_Vault/credentials/")
            return False
        
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
            creds = None
            
            # Load existing token if it exists
            if self.token_file.exists():
                self.logger.info(f"Loading existing token from {self.token_file}")
                creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
            
            # If there are no (valid) credentials, make the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    self.logger.info("Refreshing expired token")
                    creds.refresh(Request())
                else:
                    self.logger.info(f"Starting OAuth flow with {self.credentials_file}")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_file), 
                        SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                self.logger.info(f"Saving token to {self.token_file}")
                with open(self.token_file, 'w') as token:
                    token.write(creds.to_json())
            
            # Build the Gmail service
            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Gmail API authenticated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            self.logger.error("Make sure your credentials.json is valid and OAuth consent screen is configured")
            return False
    
    def check_for_updates(self) -> list:
        """Check Gmail for new urgent/important messages"""
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            # Search for unread messages (not in spam/trash)
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread -in:chats -in:drafts -in:spam -in:trash',
                maxResults=20
            ).execute()
            
            messages = results.get('messages', [])
            new_messages = []
            
            for msg in messages:
                if msg['id'] not in self.processed_ids:
                    message_data = self.get_message_details(msg['id'])
                    if message_data and self.is_important(message_data):
                        new_messages.append(message_data)
                        self.processed_ids.add(msg['id'])
                        # Limit to prevent overload
                        if len(new_messages) >= 10:
                            break
            
            return new_messages
            
        except Exception as e:
            self.logger.error(f"Error checking Gmail: {e}")
            # Try to re-authenticate on error
            self.service = None
            return []
    
    def get_message_details(self, msg_id: str) -> dict:
        """Get full message details"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            # Extract headers
            headers = {h['name']: h['value'] for h in message['payload']['headers']}
            
            # Get body
            body = self.extract_body(message['payload'])
            
            return {
                'id': msg_id,
                'from': headers.get('From', 'Unknown'),
                'to': headers.get('To', ''),
                'subject': headers.get('Subject', 'No Subject'),
                'date': headers.get('Date', ''),
                'snippet': message.get('snippet', ''),
                'body': body,
                'thread_id': message.get('threadId', '')
            }
            
        except Exception as e:
            self.logger.error(f"Error getting message details: {e}")
            return None
    
    def extract_body(self, payload) -> str:
        """Extract email body from payload"""
        body = ""
        
        if 'parts' in payload:
            # Multipart message - find the plain text part
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        data = part['body']['data']
                        body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                        break
        elif 'body' in payload:
            # Simple message
            if 'data' in payload['body']:
                data = payload['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        # If no body found, try HTML part
        if not body and 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/html':
                    if 'data' in part['body']:
                        data = part['body']['data']
                        body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                        # Remove HTML tags for plain text
                        import re
                        body = re.sub(r'<[^>]+>', '', body)
                        break
        
        return body[:2000]  # Limit body length
    
    def is_important(self, message: dict) -> bool:
        """Check if message is important based on keywords and sender"""
        text_to_check = f"{message['subject']} {message['snippet']} {message['body']}".lower()
        
        # Check for keywords
        for keyword in self.keywords:
            if keyword in text_to_check:
                return True
        
        # Check if from known important contacts/domains
        # Customize this list based on your important contacts
        important_patterns = [
            'client', 'customer', 'boss', 'manager',
            'bank', 'invoice', 'payment', 'billing',
            'support', 'noreply', 'notifications'
        ]
        
        from_address = message['from'].lower()
        for pattern in important_patterns:
            if pattern in from_address:
                return True
        
        return False
    
    def create_action_file(self, message: dict) -> Path:
        """Create a markdown action file in Needs_Action folder"""
        timestamp = datetime.now().isoformat()
        
        # Determine priority
        priority = 'high' if any(kw in message['subject'].lower() for kw in ['urgent', 'asap', 'important', 'action required']) else 'normal'
        
        # Clean subject for filename
        safe_subject = "".join(c for c in message['subject'] if c.isalnum() or c in ' -_').strip()[:50]
        if not safe_subject:
            safe_subject = "No_Subject"
        
        content = f"""---
type: email
from: {message['from']}
to: {message['to']}
subject: {message['subject']}
received: {timestamp}
gmail_id: {message['id']}
priority: {priority}
status: pending
---

## Email Received

An important email has been received and needs processing.

### Email Details
- **From**: {message['from']}
- **To**: {message['to']}
- **Subject**: {message['subject']}
- **Date**: {message['date']}
- **Priority**: {priority}
- **Gmail ID**: {message['id']}

### Email Content
```
{message['body'] if message['body'] else message['snippet']}
```

### Suggested Actions
- [ ] Read full email content
- [ ] Determine appropriate response
- [ ] Draft reply (requires approval before sending)
- [ ] Forward to relevant party if needed
- [ ] Archive after processing
- [ ] Move to Done when complete

### Notes
Add processing notes here.

---
*Created by Gmail Watcher - Silver Tier*
"""
        
        # Create action file
        action_filename = f'EMAIL_{timestamp.replace(":", "-").replace(".", "_")[:19]}_{safe_subject}.md'
        action_path = self.needs_action / action_filename
        action_path.write_text(content, encoding='utf-8')
        
        self.logger.info(f"Created action file: {action_filename}")
        return action_path
    
    def run(self):
        """Run the Gmail watcher continuously"""
        self.logger.info('Starting Gmail Watcher')
        
        if not self.google_available:
            self.logger.error("Google API libraries not available")
            print("\n❌ Google API libraries not installed!")
            print("Run: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
            print("\nOr install from requirements.txt:")
            print("  pip install -r AI_Employee_Vault/requirements.txt")
            return
        
        if not self.credentials_file.exists():
            self.logger.error(f"Credentials file not found: {self.credentials_file}")
            print(f"\n❌ Credentials file not found: {self.credentials_file}")
            print("\n📋 Setup Instructions:")
            print("1. Place your credentials.json file in: AI_Employee_Vault/credentials/")
            print("2. Make sure OAuth consent screen is configured in Google Cloud Console")
            print("3. Run the watcher again")
            return
        
        if not self.authenticate():
            self.logger.error("Failed to authenticate with Gmail")
            print("\n❌ Failed to authenticate with Gmail")
            print("\n📋 Troubleshooting:")
            print("1. Check if credentials.json is valid")
            print("2. Make sure Gmail API is enabled in Google Cloud Console")
            print("3. Check OAuth consent screen is configured")
            print("4. Delete token.json and re-authenticate")
            return
        
        print("\n✅ Gmail Watcher started successfully!")
        print(f"📬 Monitoring for urgent messages...")
        print(f"⏱️  Check interval: {self.check_interval} seconds")
        print(f"📁 Credentials: {self.credentials_file}")
        print(f"📝 Logs: {self.vault_path / 'Logs' / 'gmail_watcher.log'}")
        print("\nPress Ctrl+C to stop...\n")
        
        import time
        
        while True:
            try:
                messages = self.check_for_updates()
                if messages:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(messages)} important message(s)")
                    for message in messages:
                        action_file = self.create_action_file(message)
                        print(f"  → Created: {action_file.name}")
            except Exception as e:
                self.logger.error(f"Error in watcher loop: {e}")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
            
            time.sleep(self.check_interval)


def run_watcher(vault_path: str, check_interval: int = 120, credentials_file: str = "credentials.json"):
    """Start the Gmail watcher"""
    watcher = GmailWatcher(vault_path, check_interval, credentials_file)
    watcher.run()


if __name__ == '__main__':
    import sys
    from pathlib import Path

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        # Use absolute path - parent directory of this script
        vault_path = str(Path(__file__).parent.absolute())
    
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    credentials_file = sys.argv[3] if len(sys.argv) > 3 else "credentials.json"

    run_watcher(vault_path, check_interval, credentials_file)
