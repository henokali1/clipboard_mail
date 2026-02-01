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
POLL_INTERVAL = 1.0  # Seconds to wait between clipboard checks

# Regex pattern for email detection
EMAIL_PATTERN = re.compile(r"^(Dear|Hi|Hey)(.*)Kind regards,$", re.DOTALL | re.IGNORECASE)

def setup_logging():
    """Sets up dynamic daily logging in a nested folder structure: logs/YYYY/MM/DD-Mon-YYYY.txt"""
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day_str = now.strftime("%d-%b-%Y") # e.g., 02-Feb-2026
    
    log_dir = os.path.join("logs", year, month)
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"{day_str}.txt")
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return log_file

# Initialize logging
LOG_FILE = setup_logging()

def get_openai_client():
    """
    Initializes OpenAI client using the OPENAI_API_KEY environment variable.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        logging.error("OPENAI_API_KEY environment variable not set.")
        return None
    
    return OpenAI(api_key=api_key)

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
    
    # Capture initial clipboard state to avoid immediate re-processing on startup
    initial_text = pyperclip.paste()
    last_processed_text = initial_text.replace("\r\n", "\n").strip() if initial_text else ""
    last_rewritten_text = ""

    while True:
        try:
            # 1. Capture clipboard content
            current_text = pyperclip.paste()
            if not current_text:
                time.sleep(POLL_INTERVAL)
                continue

            # Normalize line endings and strip whitespace for robust comparison
            current_text_normalized = current_text.replace("\r\n", "\n").strip()

            # 2. Check if it matches the pattern and hasn't been processed
            if (EMAIL_PATTERN.match(current_text_normalized) and 
                current_text_normalized != last_processed_text and 
                current_text_normalized != last_rewritten_text):
                
                print(f"Email detected! Rewriting...")
                # send_notification("Email Detected", "Rewriting your email for clarity and professionalism...")
                send_notification("ED", "Rewriting...")
                
                # 3. Rewrite using OpenAI
                rewritten_text = rewrite_email(client, current_text_normalized)
                
                if rewritten_text:
                    # 4. Update clipboard
                    pyperclip.copy(rewritten_text)
                    
                    # Store normalized versions to prevent loops
                    last_processed_text = current_text_normalized
                    last_rewritten_text = rewritten_text.replace("\r\n", "\n").strip()
                    
                    # 5. Log the operation
                    logging.info(f"ORIGINAL:\n{current_text_normalized}")
                    logging.info(f"REWRITTEN:\n{last_rewritten_text}")
                    logging.info("-" * 40)
                    
                    # 6. Notify success
                    # send_notification("Success!", "Email rewritten and copied back to clipboard.")
                    send_notification("ERS!")
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
