"""
Instagram platform handler.
Uses JSON export file to cancel pending follow requests.
"""
import json
from src.utils.export_usernames import extract_usernames
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Page

from .base import Platform, PlatformConfig


class InstagramPlatform(Platform):
    """Handler for Instagram pending follow requests cancellation."""
    
    def get_targets(self) -> List[str]:
        """Load usernames from the JSON export file."""
        if not self.config.json_path:
            raise ValueError("JSON path is required for Instagram platform")
        
        with open(self.config.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return extract_usernames(data)
    
    def cancel_request(self, page: 'Page', target: str) -> bool:
        """
        Cancel a pending follow request on Instagram.
        Looks for 'Requested' button and confirms 'Unfollow'.
        """
        # Look for the Requested button
        btn = page.locator("button:has-text('Requested')")
        
        if btn.count() > 0:
            btn.first.click()
            page.wait_for_timeout(1500)
            
            # Confirm the unfollow
            confirm = page.locator("button:has-text('Unfollow')")
            if confirm.count() > 0:
                confirm.first.click()
                page.wait_for_timeout(2000)
                print(f"[✓] Cancelled {target}")
                return True
            else:
                print(f"[!] Confirm dialog not found for {target}")
        else:
            print(f"[!] No pending request found for {target}")
        
        return False
    
    def login_url(self) -> str:
        return "https://www.instagram.com/accounts/login/"
    
    def profile_url(self, target: str) -> str:
        return f"https://www.instagram.com/{target}/"
