# Professional Email Rewriter

This Python script monitors your Windows 11 clipboard for specific email patterns and automatically rewrites them into a professional version using OpenAI's ChatGPT API.

## Features

- **Automatic Detection**: Recognizes text starting with "Dear", "Hi", or "Hey" and ending with "Kind regards,".
- **AI-Powered Rewriting**: Uses OpenAI to polish and professionalize your emails.
- **Seamless Integration**: The rewritten email is automatically copied back to your clipboard.
- **Notifications**: System alerts inform you when an email is detected and when the rewriting is complete.
- **Logging**: Keeps a history of original and rewritten emails in `email_rewriter.log`.
- **Safety**: Prevents infinite loops and reprocessing the same email.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Create a `.env` file or set the following environment variables:
   - `API_USERNAME`: (Optional) Your OpenAI Organization ID.
   - `API_PASSWORD`: (Required) Your OpenAI API Key.

3. **Run the Script**:
   ```bash
   python email_rewriter.py
   ```

## Usage

1. Write a rough draft of an email. Ensure it starts with "Hi" (or "Dear"/"Hey") and ends with "Kind regards,".
2. Select the text and copy it (`Ctrl + C`).
3. Wait for the notification.
4. Paste the result (`Ctrl + V`).

## Example

**Input copied to clipboard:**
> Hi John,
>
> I won't be able to make it to the meeting today. Something came up. Let's talk tomorrow.
>
> Kind regards,

**Auto-rewritten output on clipboard:**
> Hi John,
>
> I am writing to inform you that I will be unable to attend today's scheduled meeting due to an unforeseen conflict. I would like to suggest that we reconnect tomorrow to discuss the agenda.
>
> Kind regards,
