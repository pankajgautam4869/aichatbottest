from playwright.sync_api import sync_playwright
import time
import sys

# Hardcoded values
CHATBOT_URL = 'http://localhost:8080'
CHAT_INPUT_SELECTOR = "//*[@id='chat-input']"
SEND_BUTTON_SELECTOR = "//button[@id='send-message-button']"
RESPONSE_CONTAINER = "//*[@id='response-content-container']/div[1]/p"
AUTH = {
    'email': 'pankajgautam4869@yahoo.com',
    'password': 'Openwebui@123'
}

def log_debug(message):
    """Helper function to log debug messages"""
    print(f"[DEBUG] {message}", flush=True)
    sys.stdout.flush()

def capture_new_response_paragraphs(page, prev_count):
    page.wait_for_selector(RESPONSE_CONTAINER, timeout=10000)
    paragraphs = page.query_selector_all(RESPONSE_CONTAINER)
    log_debug(f"Found {len(paragraphs)} paragraph elements")
    new_paragraphs = paragraphs[prev_count:]
    paragraph_texts = []
    for i, paragraph in enumerate(new_paragraphs, start=prev_count):
        text = paragraph.text_content()
        if text and text.strip():
            paragraph_texts.append(text.strip())
            log_debug(f"Paragraph {i+1}: {text.strip()}")
    return ' '.join(paragraph_texts)

def send_message(page, query):
    """Send a message and wait for response, with debug output and contenteditable support"""
    log_debug(f"Attempting to send message: {query}")
    page.wait_for_selector(CHAT_INPUT_SELECTOR, timeout=10000)
    try:
        chat_input = page.query_selector(CHAT_INPUT_SELECTOR)
        tag = chat_input.evaluate('el => el.tagName') if chat_input else 'N/A'
        text = chat_input.text_content() if chat_input else 'N/A'
        is_contenteditable = chat_input.get_attribute('contenteditable') if chat_input else 'N/A'
        log_debug(f"Chat input tag: {tag}, text_content before fill: {text}, contenteditable: {is_contenteditable}")
    except Exception as e:
        log_debug(f"Could not get chat input tag/text_content/contenteditable before fill: {e}")
    
    # If contenteditable, set value using JS, else try fill
    try:
        chat_input = page.query_selector(CHAT_INPUT_SELECTOR)
        is_contenteditable = chat_input.get_attribute('contenteditable') if chat_input else None
        if is_contenteditable == 'true':
            log_debug("Using JavaScript to set contenteditable value")
            page.evaluate(f"document.getElementById('chat-input').innerText = `{query}`;")
        else:
            log_debug("Using fill method to set value")
            page.fill(CHAT_INPUT_SELECTOR, query)
    except Exception as e:
        log_debug(f"Could not set chat input value: {e}")
    
    try:
        chat_input = page.query_selector(CHAT_INPUT_SELECTOR)
        text = chat_input.text_content() if chat_input else 'N/A'
        log_debug(f"text_content after fill: {text}")
    except Exception as e:
        log_debug(f"Could not get chat input text_content after fill: {e}")
    
    # Show response container before sending
    try:
        paragraphs = page.query_selector_all(RESPONSE_CONTAINER)
        log_debug(f"Response container before send: {[p.text_content() for p in paragraphs]}")
    except Exception as e:
        log_debug(f"Could not read response container before send: {e}")
    
    # Click send button with force option
    try:
        log_debug("Attempting to click send button")
        page.click(SEND_BUTTON_SELECTOR, force=True, timeout=5000)
    except Exception as e:
        log_debug(f"Warning: Could not click send button normally: {str(e)}")
        # Try alternative method
        log_debug("Trying alternative click method")
        page.evaluate("document.querySelector('#send-message-button').click()")
    
    log_debug("Waiting for response...")
    time.sleep(2)
    # Show response container after sending
    try:
        paragraphs = page.query_selector_all(RESPONSE_CONTAINER)
        log_debug(f"Response container after send: {[p.text_content() for p in paragraphs]}")
    except Exception as e:
        log_debug(f"Could not read response container after send: {e}")

def run_test():
    log_debug("Starting test execution")
    with sync_playwright() as p:
        log_debug("Launching browser")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            log_debug(f"Navigating to {CHATBOT_URL}")
            page.goto(CHATBOT_URL, wait_until='networkidle')
            
            log_debug("Waiting for login form...")
            page.wait_for_selector('input[type="email"]', timeout=10000)
            
            log_debug("Attempting login...")
            page.fill('input[type="email"]', AUTH['email'])
            page.fill('input[type="password"]', AUTH['password'])
            page.click('button[type="submit"]')
            
            log_debug("Waiting for login to complete...")
            page.wait_for_load_state('networkidle')
            
            # First question
            question1 = "Who is the Prime Minister of UAE?"
            log_debug(f"Sending first hardcoded question: {question1}")
            prev_count = len(page.query_selector_all(RESPONSE_CONTAINER))
            send_message(page, question1)
            time.sleep(5)
            response1 = capture_new_response_paragraphs(page, prev_count)
            log_debug(f"Response to first question: {response1}")
            print(f"\nResponse to first question:\n{response1}\n")

            # Second question
            question2 = "When was UAE established?"
            log_debug(f"Sending second hardcoded question: {question2}")
            prev_count = len(page.query_selector_all(RESPONSE_CONTAINER))
            send_message(page, question2)
            time.sleep(5)
            response2 = capture_new_response_paragraphs(page, prev_count)
            log_debug(f"Response to second question: {response2}")
            print(f"\nResponse to second question:\n{response2}\n")
        
        except Exception as e:
            log_debug(f"An error occurred: {str(e)}")
            page.screenshot(path="error_screenshot.png")
            raise e
        
        finally:
            log_debug("Closing browser")
            browser.close()

if __name__ == "__main__":
    log_debug("Script started")
    run_test()
    log_debug("Script completed")
