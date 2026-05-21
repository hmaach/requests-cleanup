"""
LinkedIn platform handler.
Navigates to invitation manager page to withdraw pending connection requests.
"""
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Page

from .base import Platform, PlatformConfig


class LinkedInPlatform(Platform):
    """Handler for LinkedIn pending connection requests cancellation."""
    
    def get_targets(self) -> List[str]:
        """
        For LinkedIn, targets are not individual URLs.
        We navigate to the invitation manager page and process all pending requests there.
        """
        # Return empty list - we'll process the page directly
        return []
    
    def cancel_request(self, page: 'Page', target: str = None) -> bool:
        selectors = [
            "button:has-text('Withdraw')",
            "button[aria-label*='Withdraw']",
        ]

        clicked_any = False

        for selector in selectors:
            buttons = page.locator(selector)
            count = buttons.count()

            for i in range(count):
                try:
                    btn = buttons.nth(i)
                    if not btn.is_visible():
                        continue

                    btn.click()
                    page.wait_for_timeout(1000)

                    # modal appears after click
                    dialog = page.locator("[role='dialog']")
                    dialog.wait_for(state="visible", timeout=5000)

                    confirm = dialog.locator(
                        "button:has-text('Withdraw'), "
                        "button:has-text('Yes'), "
                        "button:has-text('Confirm'), "
                        "button:has-text('Withdraw invitation')"
                    )

                    if confirm.count() > 0:
                        confirm.first.click()
                        page.wait_for_timeout(1500)
                        clicked_any = True

                except Exception:
                    continue

        return clicked_any

    def login_url(self) -> str:
        return "https://www.linkedin.com/login/"
    
    def profile_url(self, target: str) -> str:
        """Not used for LinkedIn - we use the invitation manager page."""
        return "https://www.linkedin.com/mynetwork/invitation-manager/sent/"
    
    def process_all(self, page: 'Page') -> dict:
        """
        Override to navigate to the sent invitations page.
        """
        # Navigate to the sent invitations page after login
        sent_url = "https://www.linkedin.com/mynetwork/invitation-manager/sent/"
        print(f"[*] Navigating to {sent_url}")
        page.goto(sent_url)
        page.wait_for_timeout(3000)
        
        # Process all pending requests on this page
        print(f"[*] Processing pending requests on the page...")
        
        stats = {"total": 0, "cancelled": 0, "failed": 0, "skipped": 0}
        
        # Try to click all withdraw buttons
        attempts = 0
        max_attempts = 10  # Limit iterations to avoid infinite loops
        
        while True:
            buttons = page.locator("button:has-text('Withdraw')")
            if buttons.count() == 0:
                break

            if not self.cancel_request(page):
                break

            page.wait_for_timeout(2000)
            attempts += 1

            if attempts >= max_attempts:
                break
        
        stats["total"] = stats["cancelled"]
        return stats
