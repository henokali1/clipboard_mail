# Email Rewriter Pro

Email Rewriter Pro is a background clipboard-monitoring tool that automatically detects specific prefixes (1, 2, 3, or 4) when you copy text to your clipboard. It intercepts your copied text, uses the OpenAI API to rewrite it into a professional email based on the selected mode, and instantly places the rewritten text right back into your clipboard. 

## Features
- **Seamless Background Operation**: Constantly monitors your clipboard for triggers without interrupting your workflow.
- **Audio Notifications (New)**: Plays a sound when a rewrite request is detected and a different sound when the rewritten text is successfully placed back in your clipboard.
- **Visual Alert**: Triggers system toast notifications upon start and completion.
- **Auto-Logging**: Keeps detailed daily logs in the `logs/` folder of the inputs and outputs to prevent data loss.
- **4 Custom AI Modes**: Covers everything from polishing text, addressing customer queries, to drafting responses from basic intent.

## Prerequisites

- Python 3.8+ (Windows supported as it uses `winsound`)
- An active OpenAI API Key

## Installation

1. **Clone or Download** this repository.
2. **Install the dependencies** required for clipboard interaction, environment variables, notifications, and the OpenAI API:
   ```bash
   pip install openai pyperclip plyer python-dotenv
   ```
3. **Configure Environment Variables**:
   Create a `.env` file in the same directory as the script and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Simply launch the background process using Python:
```bash
python email_rewriter.py
```

It will continuously run in the background. Whenever you intend to rewrite an email, copy the text to your clipboard, but prefix the text with one of the predefined digits (`1 `, `2 `, `3 `, or `4 `) followed by a space.

You will hear a system exclamation sound when the script detects the prefix and engages processing, and an asterisk/success sound when the new polished text is in your clipboard!

## The 4 Modes

1. **Mode 1: Professional Rewrite**
   - **Prefix:** `1 `
   - **Usage:** Highlight and copy `1 Hey John this looks bad let me fix it` 
   - **Action:** Rewrites the text to be clear, professional, concise, and conversational, while maintaining the original intent.

2. **Mode 2: Generate Reply with Subject**
   - **Prefix:** `2 `
   - **Usage:** Highlight and copy `2 I want to tell the team the meeting is moved to tomorrow`
   - **Action:** Generates a professional email reply completely from scratch with a subject line based on the rough intent you provide.

3. **Mode 3: Address Query using Draft Reply**
   - **Prefix:** `3 `
   - **Usage:** Highlight and copy `3 Yes we can do that.\n\n[Original customer query email]`
   - **Action:** Takes a quick draft reply and an original query, and intelligently rewrites your draft reply specifically to address the query email effectively and professionally.

4. **Mode 4: Rewrite with Subject Line**
   - **Prefix:** `4 `
   - **Usage:** Highlight and copy `4 Requesting a new laptop because mine is broken`
   - **Action:** Similar to Mode 1, it rewrites the email clearly and professionally, but also purposefully generates an appropriate subject line.
