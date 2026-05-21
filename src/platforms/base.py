"""
Base abstraction for social media platforms.
All platform handlers must inherit from Platform and implement required methods.
"""
import abc
from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Page


@dataclass
class PlatformConfig:
    """Configuration for platform operations."""
    headless: bool = False
    delay_seconds: float = 2.0
    json_path: Optional[str] = None
    urls: Optional[List[str]] = None


class Platform(abc.ABC):
    """Abstract base class for social media platform handlers."""
    
    def __init__(self, config: PlatformConfig):
        self.config = config
    
    @abc.abstractmethod
    def get_targets(self) -> List[str]:
        """
        Retrieve the list of targets (usernames or URLs) to process.
        For Instagram: reads from JSON file.
        For LinkedIn/Facebook: uses provided URLs.
        """
        pass
    
    @abc.abstractmethod
    def cancel_request(self, page: 'Page', target: str) -> bool:
        """
        Cancel a pending request for the given target.
        Returns True if cancelled, False otherwise.
        """
        pass
    
    @abc.abstractmethod
    def login_url(self) -> str:
        """Return the login page URL for this platform."""
        pass
    
    @abc.abstractmethod
    def profile_url(self, target: str) -> str:
        """Convert a target to a profile URL."""
        pass
    
    def process_all(self, page: 'Page') -> dict:
        """
        Process all targets and return statistics.
        """
        targets = self.get_targets()
        stats = {"total": len(targets), "cancelled": 0, "failed": 0, "skipped": 0}
        
        print(f"[*] Processing {len(targets)} targets...")
        
        for i, target in enumerate(targets, 1):
            print(f"[{i}/{len(targets)}] Processing: {target}")
            
            try:
                page.goto(self.profile_url(target))
                page.wait_for_timeout(3000)
                
                if self.cancel_request(page, target):
                    stats["cancelled"] += 1
                else:
                    stats["skipped"] += 1
                    
            except Exception as e:
                print(f"[!] Error processing {target}: {e}")
                stats["failed"] += 1
            
            # Rate limiting delay
            import time
            time.sleep(self.config.delay_seconds)
        
        return stats
