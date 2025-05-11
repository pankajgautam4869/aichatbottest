import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright
from pages.chat_page import ChatPage
import json
import time

def main():
    # Load configuration
    with open("config/config.json") as f:
        config = json.load(f)
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            ignore_https_errors=True
        )
        
        # Create new page
        page = context.new_page()
        
        # Navigate to page
        page.goto(config["base_url"])
        print(f"Navigated to {config['base_url']}")
        
        # Initialize chat page
        chat_page = ChatPage(page)
        print("Chat page initialized")
        
        # Perform login
        print("Attempting login...")
        if chat_page.login(config["auth"]["email"], config["auth"]["password"]):
            print("Login successful")
            
            # Wait for chat widget
            if chat_page.load_chat_widget():
                print("Chat widget loaded")
                
                # Send a test message
                test_message = "Hello, this is a test message"
                print(f"Sending message: {test_message}")
                if chat_page.send_message(test_message):
                    print("Message sent")
                    
                    # Wait for response
                    if chat_page.wait_for_response():
                        response = chat_page.get_last_message()
                        print(f"Received response: {response}")
                    else:
                        print("No response received")
                else:
                    print("Failed to send message")
            else:
                print("Failed to load chat widget")
        else:
            print("Login failed")
        
        # Keep browser open for inspection
        input("Press Enter to close the browser...")
        
        # Cleanup
        context.close()
        browser.close()

if __name__ == "__main__":
    main() 