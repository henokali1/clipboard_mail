# Professional Email Assistant

This Python script monitors your clipboard for message prefixes and automatically processes them using OpenAI's GPT-4o-mini API. It supports rewriting, generating replies, and polishing replies based on original queries.

## Features

- **Multi-Mode Processing**: Use numeric prefixes (`1`, `2`, `3`, `4`) to trigger different AI actions.
- **Smart Directory Logging**: Automatically organizes logs into folders by year and month (e.g., `logs/2026/02/02-Feb-2026.txt`).
- **Standard Authentication**: Uses the `OPENAI_API_KEY` environment variable.
- **Seamless Integration**: Processed text is automatically copied back to your clipboard.
- **System Notifications**: Immediate feedback via system alerts.
- **Clipboard Safety**: Prevents infinite loops and handles line-ending normalization.

## Prefix Modes

The script triggers based on the first character in your clipboard:

### `1` - Professional Rewrite
Used to polish an existing rough draft into a formal, concise version.
*   **Format**: `1 [Your rough email draft]`
*   **Output**: A polished version that maintains the original intent but uses professional language and fixed formatting.

### `2` - Generate Reply from Intent
Used to generate a full email based on a simple instruction or "intent".
*   **Format**: `2 [Your intent or instruction]`
*   **Output**: A complete professional email including a **Subject line**, a formal body, and ending with "Kind regards,".

### `3` - Rewrite Reply for Query
Used when you have a draft reply and want to ensure it properly addresses a specific query email.
*   **Format**: `3 [Your draft reply] \n\n [The original query email]`
*   **Output**: A rewritten version of your reply that is accurately tailored to the context of the query.

### `4` - Rewrite with Subject Line
Similar to Mode 1, but specifically requests a subject line for a given intent.
*   **Format**: `4 [Your intent or email text]`
*   **Output**: A professionally rewritten email that includes a relevant subject line.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the Assistant**:
   ```bash
   python email_rewriter.py
   ```

## Usage

1. Write your text in any editor (Notepad, Outlook, etc.).
2. Add the desired prefix (`1 `, `2 `, `3 `, or `4 `) at the very beginning.
3. Select the text and copy it (`Ctrl + C`).
4. Wait for the "Success!" notification.
5. Paste the result (`Ctrl + V`).

## Directory Structure
- `email_rewriter.py`: Main execution script.
- `logs/`: Contains all historical logs (ignored by Git).
  - `YYYY/MM/DD-Mon-YYYY.txt`: Daily log files.
- `.env`: Your private API keys (ignored by Git).
