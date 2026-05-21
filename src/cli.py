"""
Command-line interface for the social media request cancellation tool.
"""
import argparse
import sys
import os

from .platforms import Platform, InstagramPlatform, LinkedInPlatform, FacebookPlatform, PlatformConfig


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Cancel pending social media requests (Instagram, LinkedIn, Facebook)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Instagram (uses data/pending_follow_requests.json)
  python main.py instagram
  
  # LinkedIn (navigates to invitation manager automatically)
  python main.py linkedin
  
  # Facebook (navigates to friend requests page automatically)
  python main.py facebook
  
  # With options
  python main.py instagram --delay 3.0 --headless
  python main.py linkedin --delay 1.5
"""
    )
    
    parser.add_argument(
        "platform",
        choices=["instagram", "linkedin", "facebook"],
        help="Platform to process"
    )
    
    # Optional settings
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    
    parser.add_argument(
        "--delay", "-d",
        type=float,
        default=2.0,
        help="Delay in seconds between actions (default: 2.0)"
    )
    
    return parser.parse_args()


def get_platform(args) -> Platform:
    """Factory function to create the appropriate platform handler."""
    config = PlatformConfig(
        headless=args.headless,
        delay_seconds=args.delay,
        json_path="data/pending_follow_requests.json",
        urls=None
    )
    
    if args.platform == "instagram":
        if not os.path.exists(config.json_path):
            print(f"[ERROR] Instagram data file not found: {config.json_path}")
            print("[INFO] Place your Instagram export at that location or create it from the example:")
            print("       cp data/pending_follow_requests.json.example data/pending_follow_requests.json")
            sys.exit(1)
        return InstagramPlatform(config)
    
    elif args.platform == "linkedin":
        return LinkedInPlatform(config)
    
    elif args.platform == "facebook":
        return FacebookPlatform(config)
    
    else:
        raise ValueError(f"Unknown platform: {args.platform}")


def run(platform: Platform):
    """Run the browser automation."""
    from playwright.sync_api import sync_playwright
    
    print(f"[*] Starting {platform.__class__.__name__} request cancellation")
    print(f"[*] Login URL: {platform.login_url()}")
    print("[*] A browser window will open. Log in manually, then press ENTER in terminal...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=platform.config.headless)
        page = browser.new_page()
        
        page.goto(platform.login_url())
        input("Press ENTER after you have logged in...")
        
        stats = platform.process_all(page)
        
        print("\n" + "="*50)
        print("SUMMARY")
        print("="*50)
        print(f"Total targets:  {stats['total']}")
        print(f"Cancelled:      {stats['cancelled']}")
        print(f"Skipped:        {stats['skipped']}")
        print(f"Failed:         {stats['failed']}")
        print("="*50)
        
        browser.close()
        print("[*] Done!")


def main():
    """Main entry point."""
    try:
        args = parse_args()
        platform = get_platform(args)
        run(platform)
            
    except ValueError as e:
        print(f"[ERROR] {e}")
        print("\nUse --help for usage information.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
