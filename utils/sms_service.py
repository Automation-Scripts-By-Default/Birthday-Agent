from twilio.rest import Client
from dotenv import load_dotenv
import os
from loggin import log_error, log_info

load_dotenv(".env")

# Load credentials - supports both Auth Token and API Key methods
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_API_KEY_SID = os.getenv("TWILIO_API_KEY_SID")
TWILIO_API_KEY_SECRET = os.getenv("TWILIO_API_KEY_SECRET")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

if not TWILIO_ACCOUNT_SID or not TWILIO_PHONE_NUMBER:
    log_error("Twilio Account SID and Phone Number are required.")
    raise ValueError("Missing required Twilio credentials")

# Initialize client with either Auth Token or API Key
if TWILIO_API_KEY_SID and TWILIO_API_KEY_SECRET:
    # Use API Key authentication
    client = Client(TWILIO_API_KEY_SID,
                    TWILIO_API_KEY_SECRET, TWILIO_ACCOUNT_SID)
    log_info("Using Twilio API Key authentication")
elif TWILIO_AUTH_TOKEN:
    # Use Auth Token authentication
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    log_info("Using Twilio Auth Token authentication")
else:
    log_error("Missing Twilio authentication credentials (Auth Token or API Key).")
    raise ValueError("Missing authentication credentials")


def send_sms(to_number: str, body: str) -> str | None:
    """Send SMS using the configured Twilio phone number"""
    try:
        message = client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number,
        )
        print(f"SMS sent successfully to {to_number}. SID: {message.sid}")
        log_info(f"SMS sent successfully to {to_number}. SID: {message.sid}")
        return message.sid
    except Exception as e:
        log_error(f"Failed to send SMS to {to_number}: {e}")
        print(f"Failed to send SMS to {to_number}: {e}")
        return None
