from playwright.sync_api import sync_playwright
from time import sleep
import sys

def visit(url, admin_token):
    print("Visiting", url, file=sys.stderr)

    with sync_playwright() as p:
        # Launch a headless browser with custom Firefox preferences
        browser = p.firefox.launch(
            headless=True,
            # Make sure we don't get hacked this time
            firefox_user_prefs={
                # Prevent potential IP leaks by disabling WebRTC.
                "media.peerconnection.enabled": False,

                # Set a common User-Agent to avoid being identified as a bot or Playwright browser.
                # Note: This can also be set via the context, but it's shown here as a demonstration.
                "general.useragent.override": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) SecureBrowser/9001.0 FortressEdition/42.0 SafeFox/1337.0",

                # Block all 3rd party cookies and trackers.
                "network.cookie.cookieBehavior": 4,

                # Enforce content security policies.
                "security.csp.enable": True,

                # Increase privacy by disabling DOM storage.
                "dom.storage.enabled": False,

                # Disable unnecessary plugins to prevent fingerprinting.
                "plugin.scan.plid.all": False,

                # Disable images for faster loading if not needed. (Note: This can also be achieved using Playwright's routing)
                "permissions.default.image": 2,

                # Prevent the browser from sending the referrer in the HTTP headers.
                "network.http.sendRefererHeader": 0
            }
        )

        page = browser.new_page()

        page.set_default_timeout(3000)

        # Visit the desired URLs
        page.goto(f'http://web:8080/admin/login?token={admin_token}')
        page.goto('about:blank')
        page.goto(f'http://web:8080/viewer#{url}')

        sleep(4)

        browser.close()

