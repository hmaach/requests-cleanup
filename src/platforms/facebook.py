"""
Facebook platform handler.
Navigates to friend requests page to cancel pending requests.
"""
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Page

from .base import Platform, PlatformConfig


class FacebookPlatform(Platform):
    """Handler for Facebook pending friend requests cancellation."""
    
    def get_targets(self) -> List[str]:
        """
        For Facebook, targets are not individual URLs.
        We navigate to the friend requests page and process all pending requests there.
        """
        return []
    
    def cancel_request(self, page: 'Page', target: str = None) -> bool:
        """
        Cancel a pending friend request on Facebook.
        On the friend requests page, looks for 'Cancel' or 'Delete' buttons.
        """
        selectors = [
            "button:has-text('Cancel')",
            "button[aria-label*='Cancel request']",
            "div[aria-label*='Cancel']",
        ]
        
        clicked_any = False
        for selector in selectors:
            buttons = page.locator(selector)
            count = buttons.count()
            if count > 0:
                for i in range(count):
                    try:
                        buttons.nth(i).click()
                        page.wait_for_timeout(1500)
                        
                        # Confirm dialog if appears
                        confirm = page.locator("button:has-text('Confirm'), button:has-text('Yes'), button:has-text('Cancel')")
                        if confirm.count() > 0:
                            confirm.first.click()
                            page.wait_for_timeout(2000)
                        clicked_any = True
                    except Exception:
                        continue
        
        if clicked_any:
            print("[✓] Cancelled pending friend requests on Facebook")
        else:
            print("[!] No pending requests found on the page")
        
        return clicked_any
    
    def login_url(self) -> str:
        return "https://www.facebook.com/login/"
    
    def profile_url(self, target: str) -> str:
        """Not used for Facebook - we use the friend requests page."""
        return "https://web.facebook.com/friends/requests"
    
    def process_all(self, page: 'Page') -> dict:
        """
        Override to navigate to the friend requests page.
        """
        # Navigate to the friend requests page after login
        requests_url = "https://web.facebook.com/friends/requests"
        print(f"[*] Navigating to {requests_url}")
        page.goto(requests_url)
        page.wait_for_timeout(3000)
        
        # Process all pending requests on this page
        print(f"[*] Processing pending requests on the page...")
        
        stats = {"total": 0, "cancelled": 0, "failed": 0, "skipped": 0}
        
        # Try to click all cancel buttons
        attempts = 0
        max_attempts = 10
        
        while attempts < max_attempts:
            before_count = page.locator("button:has-text('Cancel'), button[aria-label*='Cancel request']").count()
            if before_count == 0:
                break
            
            if self.cancel_request(page):
                stats["cancelled"] += 1
                page.wait_for_timeout(2000)
            else:
                break
            
            attempts += 1
        
        stats["total"] = stats["cancelled"]
        return stats
