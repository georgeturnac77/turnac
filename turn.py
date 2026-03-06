import base64
import random
import requests
from seleniumbase import SB

# --- GEO DATA ---
geo_data = requests.get("http://ip-api.com/json/").json()
latitude = geo_data["lat"]
longitude = geo_data["lon"]
timezone_id = geo_data["timezone"]
language_code = geo_data["countryCode"].lower()

# --- DECODE NAME ---
fulln = base64.b64decode("YnJ1dGFsbGVz").decode("utf-8")
urlt = f"https://www.twitch.tv/{fulln}"

proxy_str = False


# --- HELPERS ---
def click_if_present(driver, selector, timeout=4):
    if driver.is_element_present(selector):
        driver.cdp.click(selector, timeout=timeout)
        driver.sleep(2)


def handle_consent(driver):
    click_if_present(driver, 'button:contains("Accept")')
    click_if_present(driver, 'button:contains("Start Watching")')


# --- MAIN LOOP ---
while True:
    with SB(uc=True, locale="en", ad_block=True,
            chromium_arg='--disable-webgl', proxy=proxy_str) as sb:

        sb.activate_cdp_mode(urlt, tzone=timezone_id, geoloc=(latitude, longitude))
        sb.sleep(3)

        handle_consent(sb)
        sb.sleep(10)

        # Check if stream is live
        if not sb.is_element_present("#live-channel-stream-information"):
            break

        # Open second driver
        sb2 = sb.get_new_driver(undetectable=True)
        sb2.activate_cdp_mode(urlt, tzone=timezone_id, geoloc=(latitude, longitude))
        sb2.sleep(8)
        handle_consent(sb2)

        # Random watch time
        sb.sleep(random.randint(450, 800))
