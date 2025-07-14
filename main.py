import os
import time
import requests
import openai
from playwright.sync_api import sync_playwright
from steel import Steel
from dotenv import load_dotenv
import json

load_dotenv()

try:
    client = Steel(steel_api_key=os.environ["STEEL_API_KEY"], base_url=os.getenv("STEEL_API_URL"))
except KeyError:
    raise Exception("STEEL_API_KEY environment variable not set.")
    
def analyze_result(html_content: str):
    try:
        client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    except KeyError:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    prompt = f"""
    You are an expert assistant that parses HTML and returns structured JSON.
    Analyze the following HTML from the Delaware Division of Corporations name search result page.

    From the HTML, determine:
    1. Is the business name available?
    2. What is the full status message shown on the page?
    3. What is the reservation cost?

    Return a single JSON object with these keys:
    - "is_available": boolean (true if available, false if not).
    - "status_message": string (e.g., "The name '...' is available.").
    - "cost": float (e.g., 75.00). If no cost is mentioned, use null.

    HTML to analyze:
    ---
    {html_content}
    ---
    """

    print("Sending result page HTML to OpenAI for analysis...")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are an HTML parsing assistant that only returns JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        json_response_str = response.choices[0].message.content
        return json.loads(json_response_str)
    except Exception as e:
        print(f"An error occurred while calling the OpenAI API: {e}")
        return None


def solve_captcha_with_api(session_id: str, page):
    STEEL_API_URL = os.getenv("STEEL_API_URL", "https://api.steel.dev")
    STEEL_API_KEY = os.getenv("STEEL_API_KEY")

    solve_url = f"{STEEL_API_URL}/v1/sessions/{session_id}/captchas/solve-image"
    headers = { "Content-Type": "application/json", "steel-api-key": STEEL_API_KEY }

    image_xpath = "//*[@id='ctl00_ContentPlaceHolder1_ecorpCaptcha1_captchaImage']"
    input_xpath = "//*[@id='ctl00_ContentPlaceHolder1_ecorpCaptcha1_txtCaptcha']"
    payload = { "imageXPath": image_xpath, "inputXPath": input_xpath }
    
    print("Waiting for CAPTCHA image on the page...")
    page.wait_for_selector(image_xpath, state="visible")
    print("CAPTCHA image found.")

    try:
        print(f"Sending CAPTCHA solve request to Steel API ({solve_url})...")
        response = requests.post(solve_url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()

        response_data = response.json()
        if not response_data.get("success"):
            raise Exception(f"Failed to initiate CAPTCHA solve. API message: {response_data.get('message')}")
        
        print("CAPTCHA solve request accepted. Waiting for 'Image Solved' text to appear on the page...")

        confirmation_locator = page.get_by_text("Image Solved", exact=False)
        confirmation_locator.wait_for(timeout=120000) 

        print("Found 'Image Solved' text. Proceeding with form submission.")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the Steel CAPTCHA API: {e}")
        page.screenshot(path="captcha_error_screenshot.png")
        raise
    except TimeoutError:
        print("Timeout: Did not find 'Image Solved' text on the page within the time limit.")
        page.screenshot(path="timeout_screenshot.png")
        raise

def main():
    session = None
    browser = None
    try:
        print("Creating Steel session...")
        session = client.sessions.create(solve_captcha=True)
        print(f"Session created: {session.session_viewer_url}")

        playwright = sync_playwright().start()
        print("Connecting to browser with Playwright...")
        browser = playwright.chromium.connect_over_cdp(
            f"wss://connect.steel.dev?apiKey={os.getenv('STEEL_API_KEY')}&sessionId={session.id}"
        )
        print("Successfully connected to the browser.")

        current_context = browser.contexts[0]
        page = current_context.pages[0]

        target_url = "https://icis.corp.delaware.gov/ecorp/namereserv/namereservation.aspx"
        entity_name_to_check = "GEMINI AUTOMATION SERVICES"
        
        print(f"Navigating to target URL: {target_url}")
        page.goto(target_url, wait_until="networkidle")

        print("Filling out the form...")
        page.locator("#ctl00_ContentPlaceHolder1_frmDisclaimerChkBox").check()
        print("- Checked disclaimer.")
        page.locator("#ctl00_ContentPlaceHolder1_frmEntityType").select_option("C")
        print("- Selected Entity Kind: 'CORPORATION'.")
        entity_ending_selector = "#ctl00_ContentPlaceHolder1_frmEntityEnding"
        page.locator(entity_ending_selector).wait_for(state="visible", timeout=10000)
        page.locator(entity_ending_selector).select_option("CORPORATION")
        print("- Selected Entity Ending: 'CORPORATION'.")
        page.locator("#ctl00_ContentPlaceHolder1_frmEntityName").fill(entity_name_to_check)
        print(f"- Entered Entity Name: '{entity_name_to_check}'.")

        solve_captcha_with_api(session.id, page)

        print("Submitting the form...")
        search_button_selector = "#ctl00_ContentPlaceHolder1_btnSubmit"
        page.locator(search_button_selector).click()

        print("Waiting for results page to load...")
        page.wait_for_load_state("networkidle")

        print("\n======== FINAL RESULT ========")
        html_content = page.content()
        analysis_result = analyze_result(html_content)

        if analysis_result:
            is_available = analysis_result.get("is_available")
            cost = analysis_result.get("cost")
            message = analysis_result.get("status_message", "Status message not found.")

            if is_available:
                print(f"✅ The corporate name '{entity_name_to_check}' is available for registration.")
                if cost is not None:
                    # Format the cost as currency
                    print(f"   Estimated registration cost: ${cost:.2f}")
                else:
                    print("   Cost information is not available.")
            else:
                print(f"❌ The corporate name '{entity_name_to_check}' is unavailable or already in use.")
            
            print(f"\n   (Reference) Full message analyzed by AI: \"{message}\"")

        else:
            print("Failed to get analysis from AI.")
            with open("result_page_for_manual_review.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("The result page has been saved to 'result_page_for_manual_review.html'.")

        print("==========================")

    except Exception as e:
        print(f"An error occurred during the script execution: {e}")
        if 'page' in locals() and page:
             page.screenshot(path="final_error_screenshot.png")
    finally:
        print("Closing session in 10 seconds...")
        time.sleep(10)

        if browser:
            browser.close()
            print("Browser connection closed.")
        if session:
            client.sessions.release(session.id)
            print("Steel session released.")
        print("Done!")

main()