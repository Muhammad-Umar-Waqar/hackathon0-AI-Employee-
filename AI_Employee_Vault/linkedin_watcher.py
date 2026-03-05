"""
LinkedIn Watcher - Monitors LinkedIn for notifications and posts updates
Silver Tier Implementation

Uses Playwright for browser automation to interact with LinkedIn
"""
from pathlib import Path
from datetime import datetime
import logging
import json
import time

class LinkedInWatcher:
    def __init__(self, vault_path: str, check_interval: int = 300, session_path: str = "linkedin_session"):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans_social = self.vault_path / 'Plans' / 'Social'
        self.check_interval = check_interval  # Check every 5 minutes
        # Session path - in project root credentials folder
        self.project_root = self.vault_path.parent
        self.credentials_dir = self.project_root / 'credentials'
        self.session_path = self.credentials_dir / session_path
        self.keywords = [
            'message', 'connection request', 'comment', 'mention',
            'job opportunity', 'hiring', 'partnership', 'collaboration',
            'invoice', 'payment', 'business', 'lead'
        ]
        
        # Setup logging
        self.logger = logging.getLogger('LinkedInWatcher')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.vault_path / 'Logs' / 'linkedin_watcher.log'),
                logging.StreamHandler()
            ]
        )
        
        # Ensure directories exist
        self.plans_social.mkdir(parents=True, exist_ok=True)
        self.session_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Try to import Playwright
        try:
            from playwright.sync_api import sync_playwright
            self.playwright_available = True
        except ImportError:
            self.playwright_available = False
            self.logger.warning("Playwright not installed. Run: pip install playwright && playwright install")
    
    def check_linkedin_notifications(self) -> list:
        """Check LinkedIn for new notifications using Playwright"""
        if not self.playwright_available:
            return []
        
        try:
            from playwright.sync_api import sync_playwright
            
            notifications = []
            
            with sync_playwright() as p:
                # Launch browser with persistent context (keeps login session)
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    viewport={'width': 1280, 'height': 720},
                    timeout=30000
                )
                
                page = browser.pages[0]
                
                try:
                    # Go to LinkedIn notifications
                    page.goto('https://www.linkedin.com/notifications/', timeout=30000)
                    
                    # Wait for page to load (try multiple selectors)
                    try:
                        page.wait_for_selector('.notification-card, [data-id="true"], div.artdeco-list__item', timeout=10000)
                    except:
                        # If not found, LinkedIn might be asking to login
                        if 'login' in page.url or 'checkpoint' in page.url:
                            self.logger.warning("Not logged in. Please run linkedin_login.py")
                            browser.close()
                            return []
                    
                    # Find notification cards (try multiple selectors)
                    notification_cards = page.query_selector_all('.notification-card')
                    if not notification_cards:
                        notification_cards = page.query_selector_all('div.artdeco-list__item')
                    if not notification_cards:
                        notification_cards = page.query_selector_all('[data-id="true"]')
                    
                    for card in notification_cards[:10]:  # Limit to 10 notifications
                        try:
                            notif_text = card.inner_text()
                            
                            # Check if notification is unread or important
                            if self.is_important_notification(notif_text):
                                notifications.append({
                                    'type': 'notification',
                                    'text': notif_text,
                                    'timestamp': datetime.now().isoformat()
                                })
                        except Exception:
                            continue
                    
                except Exception as e:
                    # Don't log timeout as error - it's expected when not logged in
                    if 'Timeout' not in str(type(e).__name__):
                        self.logger.warning(f"Error reading notifications: {e}")
                
                browser.close()
            
            return notifications
            
        except Exception as e:
            # Silently fail if Playwright has issues
            return []
    
    def is_important_notification(self, text: str) -> bool:
        """Check if notification is important"""
        text_lower = text.lower()
        
        # Check for keywords
        for keyword in self.keywords:
            if keyword in text_lower:
                return True
        
        return False
    
    def check_linkedin_messages(self) -> list:
        """Check LinkedIn for new messages"""
        if not self.playwright_available:
            return []
        
        try:
            from playwright.sync_api import sync_playwright
            
            messages = []
            
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    viewport={'width': 1280, 'height': 720},
                    timeout=30000
                )
                
                page = browser.pages[0]
                
                try:
                    # Go to LinkedIn messaging
                    page.goto('https://www.linkedin.com/messaging/', timeout=30000)
                    
                    # Wait for page to load
                    try:
                        page.wait_for_selector('.msg-conversation-card, [class*="conversation-card"]', timeout=10000)
                    except:
                        # If not found, LinkedIn might be asking to login
                        if 'login' in page.url or 'checkpoint' in page.url:
                            browser.close()
                            return []
                    
                    # Find conversation cards
                    conversation_cards = page.query_selector_all('.msg-conversation-card')
                    if not conversation_cards:
                        conversation_cards = page.query_selector_all('[class*="conversation-card"]')
                    
                    for card in conversation_cards[:10]:
                        try:
                            # Check if unread
                            is_unread = False
                            try:
                                is_unread = 'unread' in card.get_attribute('class') or 'selected' in card.get_attribute('class')
                            except:
                                is_unread = True  # Assume unread if we can't check
                            
                            if is_unread:
                                msg_text = card.inner_text()
                                
                                # Check for important keywords
                                if any(kw in msg_text.lower() for kw in self.keywords):
                                    messages.append({
                                        'type': 'message',
                                        'text': msg_text,
                                        'timestamp': datetime.now().isoformat()
                                    })
                        except Exception:
                            continue
                    
                except Exception as e:
                    # Don't log timeout as error
                    if 'Timeout' not in str(type(e).__name__):
                        self.logger.warning(f"Error reading messages: {e}")
                finally:
                    browser.close()
            
            return messages
            
        except Exception as e:
            # Silently fail if Playwright has issues
            return []
    
    def create_action_file(self, item: dict) -> Path:
        """Create a markdown action file in Needs_Action folder"""
        timestamp = datetime.now().isoformat()
        
        priority = 'high' if any(kw in item['text'].lower() for kw in ['urgent', 'asap', 'invoice', 'payment']) else 'normal'
        
        content = f"""---
type: linkedin_{item['type']}
received: {timestamp}
priority: {priority}
status: pending
---

## LinkedIn {item['type'].title()} Received

A LinkedIn {item['type']} has been received and needs processing.

### Details
- **Type**: {item['type']}
- **Received**: {timestamp}
- **Priority**: {priority}

### Content
```
{item['text']}
```

### Suggested Actions
- [ ] Review the {item['type']}
- [ ] Determine appropriate response
- [ ] Draft reply (requires approval before sending)
- [ ] Respond via LinkedIn
- [ ] Move to Done when complete

### Notes
Add processing notes here.

---
*Created by LinkedIn Watcher - Silver Tier*
"""
        
        # Create action file
        action_filename = f'LINKEDIN_{item["type"].upper()}_{timestamp.replace(":", "-").replace(".", "_")[:19]}.md'
        action_path = self.needs_action / action_filename
        action_path.write_text(content, encoding='utf-8')
        
        self.logger.info(f"Created action file: {action_filename}")
        return action_path
    
    def post_to_linkedin(self, content: str, image_path: str = None) -> bool:
        """Post content to LinkedIn using Playwright"""
        if not self.playwright_available:
            return False
        
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,  # Show browser for posting (user can verify)
                    viewport={'width': 1280, 'height': 720}
                )
                
                page = browser.pages[0]
                
                try:
                    # Go to LinkedIn home
                    page.goto('https://www.linkedin.com/feed/', timeout=30000)
                    
                    # Wait for post creation area
                    page.wait_for_selector('[aria-label="Start a post"]', timeout=10000)
                    
                    # Click on "Start a post"
                    page.click('[aria-label="Start a post"]')
                    
                    # Wait for text editor
                    page.wait_for_selector('[role="textbox"]', timeout=10000)
                    
                    # Type the content
                    textbox = page.query_selector('[role="textbox"]')
                    if textbox:
                        # Clear existing content
                        textbox.fill('')
                        # Type new content
                        textbox.type(content, delay=50)
                    
                    # Add image if provided
                    if image_path:
                        page.set_input_files('input[type="file"]', image_path)
                        time.sleep(2)  # Wait for upload
                    
                    # Wait for post button to be enabled
                    time.sleep(2)
                    
                    # Click post button
                    post_button = page.query_selector('button:has-text("Post")')
                    if post_button:
                        post_button.click()
                        self.logger.info("Post published successfully")
                        return True
                    else:
                        self.logger.warning("Post button not found")
                        return False
                    
                except Exception as e:
                    self.logger.error(f"Error posting to LinkedIn: {e}")
                    return False
                finally:
                    browser.close()
            
        except Exception as e:
            self.logger.error(f"Error in post_to_linkedin: {e}")
            return False
    
    def create_post_record(self, content: str, status: str = "draft") -> Path:
        """Create a post record in Plans/Social folder"""
        timestamp = datetime.now().isoformat()
        
        post_record = f"""---
type: linkedin_post
category: business_update
created: {timestamp}
scheduled: {timestamp}
status: {status}
approval_required: false
---

## Post Content
{content}

## Context
Post created via LinkedIn Watcher

## Target Audience
Business connections and followers

## Expected Outcome
Engagement and lead generation

## Approval Status
{status}

## Posted
{timestamp if status == "posted" else ""}

---
*Created by LinkedIn Watcher - Silver Tier*
"""
        
        # Create post record
        post_filename = f'POST_{timestamp.replace(":", "-").replace(".", "_")[:19]}.md'
        post_path = self.plans_social / post_filename
        post_path.write_text(post_record, encoding='utf-8')
        
        self.logger.info(f"Created post record: {post_filename}")
        return post_path
    
    def run(self):
        """Run the LinkedIn watcher continuously"""
        self.logger.info('Starting LinkedIn Watcher')
        
        if not self.playwright_available:
            self.logger.error("Playwright not available")
            print("\n❌ Playwright not installed!")
            print("Run: pip install playwright && playwright install")
            return
        
        print("\n✅ LinkedIn Watcher started!")
        print(f"📬 Monitoring for important notifications...")
        print(f"⏱️  Check interval: {self.check_interval} seconds")
        print(f"💾 Session: {self.session_path}")
        print(f"📝 Logs: {self.vault_path / 'Logs' / 'linkedin_watcher.log'}")
        print("\nPress Ctrl+C to stop...\n")
        
        import time
        
        while True:
            try:
                # Check notifications
                notifications = self.check_linkedin_notifications()
                if notifications:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(notifications)} notification(s)")
                    for notif in notifications:
                        action_file = self.create_action_file(notif)
                        print(f"  → Created: {action_file.name}")
                
                # Check messages (less frequently)
                messages = self.check_linkedin_messages()
                if messages:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(messages)} message(s)")
                    for msg in messages:
                        action_file = self.create_action_file(msg)
                        print(f"  → Created: {action_file.name}")
                        
            except Exception as e:
                self.logger.error(f"Error in watcher loop: {e}")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
            
            time.sleep(self.check_interval)


def run_watcher(vault_path: str, check_interval: int = 300):
    """Start the LinkedIn watcher"""
    watcher = LinkedInWatcher(vault_path, check_interval)
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
    
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300

    run_watcher(vault_path, check_interval)
