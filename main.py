from dotenv import load_dotenv
import os
from openai import OpenAI
import mariadb
from datetime import date
from loggin import log_error, log_info
from utils.sms_service import send_sms
from utils.email_service import send_email

load_dotenv(".env")

client = OpenAI()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

if (not EMAIL_USER or not EMAIL_PASSWORD or not OPEN_AI_KEY or
        not DB_HOST or not DB_USER or not DB_PASSWORD or not DB_NAME):
    log_error("Missing required environment variables.")
    raise ValueError("Missing required environment variables.")


family_response = None


try:
    conn = mariadb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=3306,  # Default MariaDB port
        database=DB_NAME
    )
    cursor = conn.cursor()
    log_info("Successfully connected to MariaDB Platform")
    cursor.execute("SELECT * FROM people")
    family_response = cursor.fetchall()
    conn.close()
except mariadb.Error as e:
    log_error(f"Error connecting to MariaDB Platform: {e}")
    print("Could not connect to the database, exiting.")
    exit(1)

# Generate birthday message using OpenAI
client.api_key = OPEN_AI_KEY

# Loop through family members and create birthday message if birthday is today

today = date.today()

for member in family_response:

    member_id, name, relation, birthday, phone = member

    if birthday.month == today.month and birthday.day == today.day:
        log_info(
            f"Generating birthday message for {name}, relation: {relation}")
        prompt = (f"Write a warm and heartfelt birthday message for my {relation} named {name}. "
                  "Start with Happy Birthday in swedish. Dont need to mention their name. ")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "My Name is Lucas Da Silva and you my helpful assistant that writes birthday messages. The messages should be warm, personal, and loving. Each message should be unique to the person's relation to me. The messages should be in swedish. Make it sound like it is written by me. Humanize the messages. You can use emojis if you think it is appropriate."},
                {"role": "user", "content": prompt}
            ]
        )
        birthday_message = response.choices[0].message.content

        if birthday_message is None:
            log_error(f"OpenAI returned no message for {name}.")
            continue

        # Send SMS to the person's phone number from the database
        send_sms(phone, birthday_message)
        send_email(
            subject="Happy Birthday - Script Generated Message",
            body=f"The following birthday message was sent to {name}:\n\n{birthday_message}",
            to=EMAIL_USER
        )

        log_info(f"Generated message for {name}: {birthday_message}")
