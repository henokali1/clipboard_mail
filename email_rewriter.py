import os
import time
import re
import logging
from datetime import datetime
import pyperclip
from openai import OpenAI
from plyer import notification
from dotenv import load_dotenv

# Load environment variables from .env file for local testing
load_dotenv()

# Configuration
LOG_FILE = "email_rewriter.log"
POLL_INTERVAL = 1.0  # Seconds to wait between clipboard checks

# Regex pattern for email detection
# Detects: Starts with Dear/Hi/Hey and ends with Kind regards,
# Case-insensitive, matches across multiple lines
EMAIL_PATTERN = re.compile(r"^(Dear|Hi|Hey)(.*)Kind regards,$", re.DOTALL | re.IGNORECASE)

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_openai_client():
    """
    Initializes OpenAI client using environment variables.
    Note: Standard OpenAI API uses an API Key. 
    Following user instructions to use OPENAI_API_USERNAME and OPENAI_API_PASSWORD.
    We will map OPENAI_API_PASSWORD to the API Key.
    """
    # Use PASSWORD as the API Key, USERNAME as Org ID (if applicable)
    api_key = os.getenv("OPENAI_API_PASSWORD")
    org_id = os.getenv("OPENAI_API_USERNAME")
    
    if not api_key:
        print("Error: OPENAI_API_PASSWORD environment variable not set.")
        return None
    
    return OpenAI(api_key=api_key, organization=org_id)

def send_notification(title, message):
    """Sends a system notification."""
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Email Rewriter Pro",
            timeout=5
        )
    except Exception as e:
        print(f"Failed to send notification: {e}")

def rewrite_email(client, original_text):
    """Sends the email to OpenAI for professional rewriting."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are a professional assistant that rewrites emails to be clear, professional, and concise. Maintain the original intent and tone but polish the language. Ensure the output starts exactly as provided (e.g., 'Dear [Name]') and ends exactly with 'Kind regards,'."},
                {"role": "user", "content": f"Please rewrite the following email professionally:\n\n{original_text}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenAI Error: {e}")
        return None

def main():
    client = get_openai_client()
    if not client:
        return

    print("Email Rewriter is running. Monitoring clipboard for 'Dear/Hi/Hey ... Kind regards,'...")
    
    last_processed_text = ""
    last_rewritten_text = ""

    while True:
        try:
            # 1. Capture clipboard content
            current_text = pyperclip.paste()
            if not current_text:
                time.sleep(POLL_INTERVAL)
                continue

            # Strip whitespace for comparison
            current_text_stripped = current_text.strip()

            # 2. Check if it matches the pattern and hasn't been processed
            # We also ensure we don't re-process the text we just outputted
            if (EMAIL_PATTERN.match(current_text_stripped) and 
                current_text_stripped != last_processed_text and 
                current_text_stripped != last_rewritten_text):
                
                print(f"Email detected! Rewriting...")
                send_notification("Email Detected", "Rewriting your email for clarity and professionalism...")
                
                # 3. Rewrite using OpenAI
                rewritten_text = rewrite_email(client, current_text_stripped)
                
                if rewritten_text:
                    # 4. Update clipboard
                    pyperclip.copy(rewritten_text)
                    
                    # Store to prevent loops
                    last_processed_text = current_text_stripped
                    last_rewritten_text = rewritten_text.strip()
                    
                    # 5. Log the operation
                    logging.info(f"ORIGINAL:\n{current_text_stripped}")
                    logging.info(f"REWRITTEN:\n{rewritten_text}")
                    logging.info("-" * 40)
                    
                    # 6. Notify success
                    send_notification("Success!", "Email rewritten and copied back to clipboard.")
                    print("Successfully rewritten and copied back to clipboard.")
                else:
                    print("Failed to rewrite email. Check logs for details.")

            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            print("\nStopping Email Rewriter.")
            break
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
