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

# Multi-mode Regex patterns
# Mode 1: "1 <email_text>" -> Rewrite professionally
# Mode 2: "2 <intent_text>" -> Generate reply email with subject
# Mode 3: "3 <reply_to_rewrite>\n\n<original_query>" -> Rewrite reply for query
# Mode 4: "4 <intent_text>" -> Rewrite with subject line
MODE_PATTERN = re.compile(r"^([1234])\s+(.*)$", re.DOTALL | re.IGNORECASE)

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

def send_notification(title, message=""):
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

def process_email(client, mode, content):
    """Handles different processing modes using OpenAI."""
    try:
        system_prompt = "You are a professional assistant."
        user_prompt = ""

        if mode == "1":
            system_prompt = "You are a professional assistant that rewrites emails to be clear, professional, and concise. Maintain the original intent and tone but polish the language. Ensure the output starts exactly as provided (e.g., 'Dear [Name]') and ends exactly with 'Kind regards,'. Use simple, clear language and avoid unnecessary words, filler phrases, dashes, or decorative characters. Keep the tone formal and respectful. Do not mention things like I hope this message finds you well. Do not add emojis or extra formatting."
            user_prompt = f"Please rewrite the following email professionally:\n\n{content}"
        
        elif mode == "2":
            system_prompt = "You are a professional assistant. Write a professional and polite email that is concise and direct. Use simple, clear language and avoid unnecessary words, filler phrases, dashes, or decorative characters. Keep the tone formal and respectful. Do not mention things like I hope this message finds you well. Do not add emojis or extra formatting, ending with 'Kind regards,'. Do not add a place holder like [Your Name] after Kind regards,"
            user_prompt = f"Generate a professional email reply with a subject line for the following intent:\n\n{content}"
            
        elif mode == "3":
            system_prompt = "You are a professional assistant. Write a professional and polite email that is concise and direct. You will be provided with a draft reply and the original query email. Rewrite the draft reply to addresses the query by using simple, clear language and avoid unnecessary words, filler phrases, dashes, or decorative characters. Keep the tone formal and respectful. Do not mention things like I hope this message finds you well. Do not add emojis or extra formatting, ending with 'Kind regards,'. Do not add a place holder like [Your Name] after Kind regards,"
            user_prompt = f"Rewrite the following reply email specifically to address the query email provided below:\n\n{content}"

        elif mode == "4":
            system_prompt = "You are a professional assistant that rewrites emails to be clear, professional, and concise. Maintain the original intent and tone but polish the language. Ensure the output starts exactly as provided (e.g., 'Dear [Name]') and ends exactly with 'Kind regards,'. Use simple, clear language and avoid unnecessary words, filler phrases, dashes, or decorative characters. Keep the tone formal and respectful. Do not mention things like I hope this message finds you well. Do not add emojis or extra formatting."
            user_prompt = f"Please rewrite the following email with a subject line for the following intent:\n\n{content}"

        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
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

    print("Email Rewriter is running. Use prefixes (1, 2, 3, 4) followed by your text...")
    
    # Capture initial clipboard state to avoid immediate re-processing on startup
    initial_text = pyperclip.paste()
    last_processed_text = initial_text.replace("\r\n", "\n").strip() if initial_text else ""
    last_rewritten_text = ""

    send_notification("ER Started!", "")

    while True:
        try:
            # 1. Capture clipboard content
            current_text = pyperclip.paste()
            if not current_text:
                time.sleep(POLL_INTERVAL)
                continue

            # Normalize line endings and strip whitespace for robust comparison
            current_text_normalized = current_text.replace("\r\n", "\n").strip()

            # 2. Check if it matches the prefix pattern and hasn't been processed
            match = MODE_PATTERN.match(current_text_normalized)
            if (match and 
                current_text_normalized != last_processed_text and 
                current_text_normalized != last_rewritten_text):
                
                mode = match.group(1)
                content = match.group(2).strip()
                
                print(f"Prefix {mode} detected! Processing...")
                send_notification("Email Tool", f"Processing Mode {mode}...")
                
                # 3. Process using OpenAI
                processed_text = process_email(client, mode, content)
                
                if processed_text:
                    # 4. Update clipboard
                    pyperclip.copy(processed_text)
                    
                    # Store normalized versions to prevent loops
                    last_processed_text = current_text_normalized
                    last_rewritten_text = processed_text.replace("\r\n", "\n").strip()
                    
                    # 5. Log the operation
                    logging.info(f"MODE: {mode}")
                    logging.info(f"INPUT:\n{content}")
                    logging.info(f"OUTPUT:\n{processed_text}")
                    logging.info("-" * 40)
                    
                    # 6. Notify success
                    send_notification("Success!", "")
                    print("Successfully processed and copied back to clipboard.")
                else:
                    print("Failed to process. Check logs for details.")

            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            print("\nStopping Email Rewriter.")
            break
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
            time.sleep(POLL_INTERVAL)

            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            print("\nStopping Email Rewriter.")
            break
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
